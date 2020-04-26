from typing import List, Dict, Tuple, Callable
from collections import namedtuple

from attribute_system import get_attribute_autogen_function, get_attribute_import_function
from abstract_class.absract_class import AbstractClass
from class_desc_gen.plugins.python_autogen.types import from_string_to_built_in_type
from class_desc_gen.types_converter import get_language_type

_JINJA_PROPERTY = namedtuple("_JINJA_PROPERTY", ["name", "val", "const", "type", "camel_case_name", "camel_case_name_f_l"])

_STATIC_VAR_ATTRIBUTE_NAME = "static"
_CONST_VAR_ATTRIBUTE_NAME = "const"


def from_underscore_to_camel_case(string: str) -> str:
    return ''.join(x.capitalize() or '_' for x in string.split('_'))


def collect_properties_names(abstract_class: AbstractClass) -> List[str]:
    return [prop.name for prop in abstract_class.properties]


def collect_properties_types(abstract_class: AbstractClass) -> Dict:
    res = dict()
    for prop in abstract_class.properties:
        res[prop.name] = prop.type
    return res


def collect_properties_attributes(abstract_class: AbstractClass) -> Dict:
    res = {}
    for prop in abstract_class.properties:
        cur_attrs = dict()
        for attr in prop.attrs:
            cur_attrs[attr.name] = str(attr.val)
        res[prop.name] = cur_attrs
    return res


def _collect_properties_with_static_flag(abstract_class: AbstractClass, static_flag: bool, target_lan: str) -> List[_JINJA_PROPERTY]:
    res = []
    for prop in abstract_class.properties:
        val = None
        is_const = False
        is_static = False

        for attr in prop.attrs:
            if attr.name == _STATIC_VAR_ATTRIBUTE_NAME:
                is_static = True

            if attr.name == _CONST_VAR_ATTRIBUTE_NAME:
                is_const = True
                val = attr.val
                break

        if is_static != static_flag:
            continue

        if val is not None:
            val_built_in_type = from_string_to_built_in_type(prop.type)
            val = val_built_in_type(val)

        if isinstance(val, str):
            val = '"%s"' % val
        elif val is None:
            if target_lan == 'java':
                val = 'null'
        camel_case_name = from_underscore_to_camel_case(prop.name)
        camel_case_name_f_l = camel_case_name[0].lower() + camel_case_name[1:]
        res.append(_JINJA_PROPERTY(name=prop.name,
                                   val=val,
                                   const=is_const,
                                   type=get_language_type(prop.type, target_lan),
                                   camel_case_name=camel_case_name,
                                   camel_case_name_f_l=camel_case_name_f_l))
    return res


def collect_static_properties(abstract_class: AbstractClass, target_lan: str) -> List[_JINJA_PROPERTY]:
    return _collect_properties_with_static_flag(abstract_class=abstract_class, static_flag=True, target_lan=target_lan)


def collect_properties(abstract_class: AbstractClass, target_lan: str) -> List[_JINJA_PROPERTY]:
    return _collect_properties_with_static_flag(abstract_class=abstract_class, static_flag=False, target_lan=target_lan)


def collect_all_class_attrs_functions(abstract_class: AbstractClass, target_lan: str) -> Tuple[List[Tuple[Callable, str]], List[Callable]]:
    class_attrs_autogen_functions = []
    class_attrs_import_function = []
    for class_attr in abstract_class.attrs:
        class_attrs_autogen_functions.append((get_attribute_autogen_function(attribute_name=class_attr.name,
                                                                             target_lan=target_lan),
                                              class_attr.name))
        class_attrs_import_function.append(get_attribute_import_function(attribute_name=class_attr.name,
                                                                         target_lan=target_lan))

    return class_attrs_autogen_functions, class_attrs_import_function

