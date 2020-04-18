from typing import Type
from enum import Enum


class Types(Enum):
    STRING = 0,
    INT    = 1,
    BOOL   = 2,
    FLOAT  = 3


_CUSTOM_TO_BUILT_IN_TYPE = {
    Types.STRING: type(''),
    Types.INT:    type(1),
    Types.BOOL:   type(True),
    Types.FLOAT:  type(1.0),
}

_STRING_TO_CUSTOM_TYPE = {
    "str":    Types.STRING,
    "int":    Types.INT,
    "bool":   Types.BOOL,
    "float":  Types.FLOAT,
}


def from_string_to_custom_type(string: str) -> Types:
    return _STRING_TO_CUSTOM_TYPE[string]


def from_custom_type_to_built_in_type(custom_type: Types) -> Type:
    return _CUSTOM_TO_BUILT_IN_TYPE[custom_type]


def from_string_to_built_in_type(string: str) -> Type:
    return from_custom_type_to_built_in_type(from_string_to_custom_type(string))
