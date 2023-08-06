import ast
from typing import List, Tuple, Union

from graphql import (
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLScalarType,
    GraphQLSchema,
    ListTypeNode,
    NamedTypeNode,
    NonNullTypeNode,
    TypeNode,
    VariableDefinitionNode,
)

from ..exceptions import ParsingError
from .codegen import (
    generate_annotation_name,
    generate_arg,
    generate_arguments,
    generate_constant,
    generate_dict,
    generate_list_annotation,
    generate_name,
)
from .constants import ANY, SIMPLE_TYPE_MAP
from .utils import str_to_snake_case


class ArgumentsGenerator:
    def __init__(
        self, schema: GraphQLSchema, convert_to_snake_case: bool = True
    ) -> None:
        self.schema = schema
        self.convert_to_snake_case = convert_to_snake_case
        self.used_types: List[str] = []
        self._used_enums: List[str] = []
        self._used_inputs: List[str] = []

    def generate(
        self, variable_definitions: Tuple[VariableDefinitionNode, ...]
    ) -> Tuple[ast.arguments, ast.Dict]:
        """Generate arguments from given variable definitions."""
        arguments = generate_arguments([generate_arg("self")])
        dict_ = generate_dict()
        for variable_definition in variable_definitions:
            org_name = variable_definition.variable.name.value
            name = self._process_name(org_name)
            annotation = self._parse_type_node(variable_definition.type)

            arguments.args.append(generate_arg(name, annotation))
            dict_.keys.append(generate_constant(org_name))
            dict_.values.append(generate_name(name))
        return arguments, dict_

    def get_used_enums(self) -> List[str]:
        return self._used_enums

    def get_used_inputs(self) -> List[str]:
        return self._used_inputs

    def _process_name(self, name: str) -> str:
        if self.convert_to_snake_case:
            return str_to_snake_case(name)
        return name

    def _parse_type_node(
        self,
        node: Union[NamedTypeNode, ListTypeNode, NonNullTypeNode, TypeNode],
        nullable: bool = True,
    ) -> Union[ast.Name, ast.Subscript]:
        if isinstance(node, NamedTypeNode):
            return self._parse_named_type_node(node, nullable)

        if isinstance(node, ListTypeNode):
            return generate_list_annotation(
                self._parse_type_node(node.type, nullable), nullable
            )

        if isinstance(node, NonNullTypeNode):
            return self._parse_type_node(node.type, False)

        raise ParsingError("Invalid argument type.")

    def _parse_named_type_node(
        self, node: NamedTypeNode, nullable: bool = True
    ) -> Union[ast.Name, ast.Subscript]:
        name = node.name.value
        type_ = self.schema.type_map.get(name)
        if not type_:
            raise ParsingError(f"Argument type {name} not found in schema.")

        if isinstance(type_, GraphQLInputObjectType):
            self._used_inputs.append(name)
        elif isinstance(type_, GraphQLEnumType):
            self._used_enums.append(name)
        elif isinstance(type_, GraphQLScalarType):
            name = SIMPLE_TYPE_MAP.get(name, ANY)
        else:
            raise ParsingError(f"Incorrect argument type {name}")

        return generate_annotation_name(name, nullable)
