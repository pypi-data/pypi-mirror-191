import typing as tp
from collections import defaultdict
import copy

import mypy.nodes
import mypy.types


annotation_node_dict: tp.Dict[str, "AnnotationNode"] = {}
type_vars_of_node: tp.Dict[str, tp.List[str]] = defaultdict(list)
any_type_instance = mypy.types.AnyType(mypy.types.TypeOfAny.unannotated)


class Annotation:
    node_id_key = "nodeId"
    args_key = "args"  # optional

    def __init__(self, node_id, args: tp.Optional[tp.List['Annotation']] = None):
        self.node_id = node_id
        self.args = args

    def encode(self):
        result = {self.node_id_key: str(self.node_id)}
        if self.args is not None:
            result[self.args_key] = [x.encode() for x in self.args]
        return result


class AnnotationNode:
    type_key = 'type'

    def __init__(self, annotation_type, id_, meta: 'Meta'):
        self.type = annotation_type
        self.id_ = id_
        annotation_node_dict[id_] = self
        self.meta = copy.deepcopy(meta)

    def encode(self):
        return {self.type_key: self.type}

    def __eq__(self, other):
        return self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)


class Definition:
    kind_key = 'kind'

    def __init__(self, kind: str, meta: 'Meta'):
        self.kind = kind
        self.meta = copy.deepcopy(meta)

    def encode(self):
        return {self.kind_key: self.kind}


class Variable(Definition):
    kind = 'Variable'

    name_key = 'name'
    is_property_key = 'isProperty'
    is_self_key = 'isSelf'
    type_key = 'type'

    def __init__(self, var: mypy.nodes.Var, meta: 'Meta'):
        super().__init__(self.kind, meta)
        self.name: str = var.name
        self.is_property: bool = var.is_property
        self.is_self: bool = var.is_self
        self.type: Annotation
        if var.type is None or self.meta.is_arg:
            self.type = get_annotation(any_type_instance, self.meta)
        else:
            self.type = get_annotation(var.type, self.meta)

    def encode(self):
        superclass_dict = super().encode()
        subclass_dict = {
            self.name_key: self.name,
            self.is_property_key: self.is_property,
            self.is_self_key: self.is_self,
            self.type_key: self.type.encode()
        }
        return dict(superclass_dict, **subclass_dict)


class ClassDef(Definition):
    kind = 'ClassDef'

    type_key = 'type'

    def __init__(self, type_info: mypy.nodes.TypeInfo, meta: 'Meta'):
        super().__init__(self.kind, meta)
        self.type: Annotation = get_annotation(mypy.types.Instance(type_info, []), self.meta)

    def encode(self):
        superclass_dict = super().encode()
        subclass_dict = {self.type_key: self.type.encode()}
        return dict(superclass_dict, **subclass_dict)


class FuncDef(Definition):
    kind = 'FuncDef'

    type_key = 'type'
    args_key = 'args'
    name_key = 'name'

    def __init__(self, func_def: mypy.nodes.FuncDef, meta: 'Meta'):
        super().__init__(self.kind, meta)
        self.type: Annotation

        if func_def.type is None:
            node = FunctionNode(str(id(func_def)), self.meta, func_def)
            self.type = Annotation(node.id_)
        else:
            self.type = get_annotation(func_def.type, self.meta)

        self.args: tp.List[Definition] = []
        self.name: str = func_def.name
        self.meta.is_arg = True
        for x in func_def.arguments:
            defn = get_definition_from_node(x.variable, self.meta)
            assert defn is not None
            self.args.append(defn)
        self.meta.is_arg = False

    def encode(self):
        superclass_dict = super().encode()
        subclass_dict = {
            self.args_key: [x.encode() for x in self.args],
            self.type_key: self.type.encode(),
            self.name_key: self.name
        }
        return dict(superclass_dict, **subclass_dict)


class OverloadedFuncDef(Definition):
    kind = 'OverloadedFuncDef'

    type_key = 'type'
    items_key = 'items'
    name_key = 'name'

    def __init__(self, func_def: mypy.nodes.OverloadedFuncDef, meta: 'Meta'):
        super().__init__(self.kind, meta)
        self.type: Annotation
        if func_def.type is None:
            self.type = get_annotation(any_type_instance, self.meta)
        else:
            self.type = get_annotation(func_def.type, self.meta)
        
        self.items: tp.List[Definition] = []
        for x in func_def.items:
            cur = get_definition_from_node(x, self.meta)
            assert cur is not None
            self.items.append(cur)
        
        self.name: str = func_def.name

    def encode(self):
        superclass_dict = super().encode()
        subclass_dict = {
            self.type_key: self.type.encode(),
            self.items_key: [x.encode() for x in self.items],
            self.name_key: self.name
        }
        return dict(superclass_dict, **subclass_dict)


class TypeVarNode(AnnotationNode):
    annotation_type = 'TypeVar'

    var_name_key = 'varName'
    values_key = 'values'
    upper_bound_key = 'upperBound'
    def_key = 'def'
    variance_key = 'variance'

    # variance values
    covariant = "COVARIANT"
    contravariant = "CONTRAVARIANT"
    invariant = "INVARIANT"

    def __init__(self, type_var: mypy.types.TypeVarType, id_: str, meta: 'Meta'):
        super().__init__(self.annotation_type, id_, meta)
        self.name: str = type_var.name
        self.values: tp.List[Annotation] = [
            get_annotation(x, self.meta)
            for x in type_var.values
        ]
        self.def_id: str = self.meta.fullname_to_node_id[type_var.id.namespace]
        type_vars_of_node[self.def_id].append(id_)
        self.upper_bound: Annotation = get_annotation(type_var.upper_bound, self.meta)
        self.variance: str
        if type_var.variance == mypy.nodes.COVARIANT:
            self.variance = self.covariant
        elif type_var.variance == mypy.nodes.CONTRAVARIANT:
            self.variance = self.contravariant
        else:
            self.variance = self.invariant

    def encode(self):
        superclass_dict = super().encode()
        subclass_dict = {
            self.var_name_key: self.name,
            self.values_key: [x.encode() for x in self.values],
            self.upper_bound_key: self.upper_bound.encode(),
            self.def_key: self.def_id,
            self.variance_key: self.variance
        }
        return dict(superclass_dict, **subclass_dict)


class FunctionNode(AnnotationNode):
    annotation_type = 'Function'

    type_vars_key = 'typeVars'
    arg_types_key = 'argTypes'
    return_type_key = 'returnType'
    arg_kinds_key = 'argKinds'
    arg_names_key = 'argNames'

    # argKinds values
    arg_pos = "ARG_POS"
    arg_opt = "ARG_OPT"
    arg_star = "ARG_STAR"
    arg_star_2 = "ARG_STAR_2"
    arg_named = "ARG_NAMED"
    arg_named_opt = "ARG_NAMED_OPT"  # TODO: is it needed?

    def __init__(self, id_: str, meta: 'Meta', type: tp.Union[mypy.types.CallableType, mypy.nodes.FuncItem]):
        super().__init__(self.annotation_type, id_, meta)
        self.type_vars: tp.List[str]
        self.arg_types: tp.List[Annotation]
        self.return_type: Annotation
        self.arg_kinds: tp.List[str]
        self.arg_names: tp.List[tp.Optional[str]]

        self.meta.fullname_to_node_id[''] = id_

        if isinstance(type, mypy.types.CallableType):
            self.arg_types = [get_annotation(x, meta=self.meta) for x in type.arg_types]
            self.return_type = get_annotation(type.ret_type, self.meta)
            self.arg_kinds = [self._get_arg_kind(x) for x in type.arg_kinds]
            self.arg_names = type.arg_names
            self.type_vars = type_vars_of_node[id_]
        elif isinstance(type, mypy.nodes.FuncItem):
            self.type_vars = []
            first_arg = []
            if len(type.arguments) and type.arguments[0].variable.is_self:
                first_arg = [Annotation(self.meta.containing_class)]
            elif len(type.arguments):
                first_arg = [get_annotation(any_type_instance, meta=self.meta)]
            
            self.arg_types = first_arg + [get_annotation(any_type_instance, meta=self.meta) for _ in type.arguments[1:]]
            self.return_type = get_annotation(any_type_instance, meta=self.meta)
            self.arg_kinds = [self._get_arg_kind(x) for x in type.arg_kinds]
            self.arg_names = type.arg_names
        else:
            assert False, "Not reachable"
    
    def _get_arg_kind(self, kind):
        if kind == mypy.nodes.ARG_POS:
            return self.arg_pos
        elif kind == mypy.nodes.ARG_OPT:
            return self.arg_opt
        elif kind == mypy.nodes.ARG_STAR:
            return self.arg_star
        elif kind == mypy.nodes.ARG_STAR2:
            return self.arg_star_2
        elif kind == mypy.nodes.ARG_NAMED_OPT:
            return self.arg_named_opt
        elif kind == mypy.nodes.ARG_NAMED:
            return self.arg_named
        else:
            assert False, "Not reachable"

    def encode(self):
        superclass_dict = super().encode()
        subclass_dict = {
            self.type_vars_key: self.type_vars,
            self.arg_types_key: [x.encode() for x in self.arg_types],
            self.return_type_key: self.return_type.encode(),
            self.arg_kinds_key: self.arg_kinds,
            self.arg_names_key: self.arg_names
        }
        return dict(superclass_dict, **subclass_dict)


class CompositeAnnotationNode(AnnotationNode):
    module_key = 'module'
    simple_name_key = 'simpleName'
    members_key = 'members'
    type_vars_key = 'typeVars'
    bases_key = 'bases'

    def __init__(self, annotation_type: str, symbol_node: mypy.nodes.TypeInfo, id_, meta: 'Meta'):
        super().__init__(annotation_type, id_, meta)
        self.meta.fullname_to_node_id[symbol_node._fullname] = id_
        self.module: str = symbol_node.module_name
        self.simple_name: str = symbol_node._fullname[len(self.module)+1:]

        self.meta.containing_class = id_
        self.members: tp.List[Definition] = []
        for name in symbol_node.names.keys():
            inner_node = symbol_node.names[name].node
            if inner_node is None:
                continue
            definition = get_definition_from_node(inner_node, self.meta)
            if definition is not None:
                self.members.append(definition)
        
        self.meta.containing_class = None

        self.raw_type_vars: tp.Sequence[mypy.types.Type] = symbol_node.defn.type_vars
        self.type_vars: tp.List[Annotation] = [
            get_annotation(x, self.meta) for x in self.raw_type_vars
        ]
        self.bases: tp.List[Annotation] = [get_annotation(x, self.meta) for x in symbol_node.bases]

    def encode(self):
        superclass_dict = super().encode()
        subclass_dict = {
            self.module_key: self.module,
            self.simple_name_key: self.simple_name,
            self.members_key: [x.encode() for x in self.members],
            self.type_vars_key: [x.encode() for x in self.type_vars],
            self.bases_key: [x.encode() for x in self.bases]
        }
        return dict(superclass_dict, **subclass_dict)


class ConcreteAnnotationNode(CompositeAnnotationNode):
    annotation_type = 'Concrete'

    is_abstract_key = 'isAbstract'

    def __init__(self, symbol_node: mypy.nodes.TypeInfo, id_, meta: 'Meta'):
        assert not symbol_node.is_protocol
        super().__init__(self.annotation_type, symbol_node, id_, meta)
        self.is_abstract: bool = symbol_node.is_abstract

    def encode(self):
        superclass_dict = super().encode()
        subclass_dict = {self.is_abstract_key: self.is_abstract}
        return dict(superclass_dict, **subclass_dict)


class ProtocolAnnotationNode(CompositeAnnotationNode):
    annotation_type = 'Protocol'

    member_names_key = 'protocolMembers'

    def __init__(self, symbol_node: mypy.nodes.TypeInfo, id_, meta: 'Meta'):
        assert symbol_node.is_protocol
        super().__init__(self.annotation_type, symbol_node, id_, meta)
        self.member_names: tp.List[str] = symbol_node.protocol_members

    def encode(self):
        superclass_dict = super().encode()
        subclass_dict = {self.member_names_key: self.member_names}
        return dict(superclass_dict, **subclass_dict)


class AnnotationNodeWithItems(AnnotationNode):
    items_key = 'items'

    def __init__(self, annotation_type: str, mypy_type, id_, namespace: 'Meta'):
        super().__init__(annotation_type, id_, namespace)
        self.items: tp.List[Annotation] = [
            get_annotation(x, self.meta) for x in mypy_type.items
        ]

    def encode(self):
        superclass_dict = super().encode()
        subclass_dict = {self.items_key: [x.encode() for x in self.items]}
        return dict(superclass_dict, **subclass_dict)


class Meta:
    def __init__(self, module_name: str, is_arg: bool = False):
        self.fullname_to_node_id: tp.Dict[str, str] = {}
        self.module_name = module_name
        self.is_arg = is_arg
        self.containing_class = None


def get_annotation_node(mypy_type: mypy.types.Type, meta: Meta) -> AnnotationNode:

    if isinstance(mypy_type, mypy.types.Instance):
        id_ = str(id(mypy_type.type))
    elif isinstance(mypy_type, mypy.types.TypeVarType):
        if mypy_type.id.namespace not in meta.fullname_to_node_id.keys():
            id_ = '0'
            mypy_type = mypy.types.Type()
        else:
            node = meta.fullname_to_node_id[mypy_type.id.namespace]
            id_ = '.' + str(mypy_type.id.raw_id) + '.' + node
    elif isinstance(mypy_type, mypy.types.AnyType):
        id_ = 'A'
    elif isinstance(mypy_type, mypy.types.NoneType):
        id_ = 'N'
    else:
        id_ = str(id(mypy_type))

    if id_ in annotation_node_dict.keys():
        return annotation_node_dict[id_]

    result: AnnotationNode

    if isinstance(mypy_type, mypy.types.Instance):
        if mypy_type.type.is_protocol:
            result = ProtocolAnnotationNode(mypy_type.type, id_, meta)
        else:
            result = ConcreteAnnotationNode(mypy_type.type, id_, meta)
    elif isinstance(mypy_type, mypy.types.CallableType):
        result = FunctionNode(id_, meta, mypy_type)

    elif isinstance(mypy_type, mypy.types.Overloaded):  # several signatures for one function
        result = AnnotationNodeWithItems("Overloaded", mypy_type, id_, meta)
    
    elif isinstance(mypy_type, mypy.types.TypeVarType):
        result = TypeVarNode(mypy_type, id_, meta)

    elif isinstance(mypy_type, mypy.types.AnyType):
        result = AnnotationNode("Any", id_, meta)

    elif isinstance(mypy_type, mypy.types.TupleType):
        result = AnnotationNodeWithItems("Tuple", mypy_type, id_, meta)

    elif isinstance(mypy_type, mypy.types.UnionType):
        result = AnnotationNodeWithItems("Union", mypy_type, id_, meta)

    elif isinstance(mypy_type, mypy.types.NoneType):
        result = AnnotationNode("NoneType", id_, meta)

    elif isinstance(mypy_type, mypy.types.TypeAliasType) and \
            mypy_type.alias is not None:
        return get_annotation_node(mypy_type.alias.target, meta)

    else:
        id_ = '0'
        result = AnnotationNode("Unknown", id_, meta)

    annotation_node_dict[id_] = result
    return result


def get_annotation(mypy_type: mypy.types.Type, meta: Meta) -> Annotation:
    cur_node = get_annotation_node(mypy_type, meta)

    if isinstance(mypy_type, mypy.types.Instance):
        children = []
        for arg in mypy_type.args:
            children.append(get_annotation(arg, meta))

        if len(children) == 0:
            return Annotation(cur_node.id_)
        else:
            return Annotation(cur_node.id_, children)

    # TODO: consider LiteralType
    
    else:
        return Annotation(cur_node.id_)


def get_definition_from_node(node: mypy.nodes.Node, meta: Meta, only_types: bool = False) -> tp.Optional[Definition]:
    if isinstance(node, mypy.nodes.TypeInfo):
        return ClassDef(node, meta)
    elif not only_types and isinstance(node, mypy.nodes.FuncDef):
        return FuncDef(node, meta)
    elif not only_types and isinstance(node, mypy.nodes.OverloadedFuncDef):
        return OverloadedFuncDef(node, meta)
    elif not only_types and isinstance(node, mypy.nodes.Var):
        return Variable(node, meta)
    elif not only_types and isinstance(node, mypy.nodes.Decorator):
        return Variable(node.var, meta)
    else:
        return None


def get_definition_from_symbol_node(
    table_node: mypy.nodes.SymbolTableNode,
    meta: Meta,
    only_types: bool = False
)-> tp.Optional[Definition]:
    if table_node.node is None or not (table_node.node.fullname.startswith(meta.module_name)) \
            or not isinstance(table_node.node, mypy.nodes.Node):  # this check is only for mypy
        return None

    return get_definition_from_node(table_node.node, meta, only_types)