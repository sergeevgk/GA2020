import os
import shutil

from collections import namedtuple
from typing import List, Tuple, Dict, Callable
from functools import partial
from jinja2 import Environment, FileSystemLoader

from abstract_class.absract_class import AbstractClass, AbstractMethod
from class_desc_gen._config_parser import _PluginParams
from class_desc_gen.types_converter import get_language_type
from attribute_system import get_attribute_autogen_function, get_attribute_options, get_attribute_import_function

from class_desc_gen.plugins.python_autogen.types import from_string_to_built_in_type


_JINJA_TEMPLATES_DIR_PATH = "./class_desc_gen/plugins/python_autogen/templates"
_JINJA_DESC_CLASS_TEMPLATE_NAME = "desc_class_py.jinja2"
_JINJA_ABSTRACT_CLASS_TEMPLATE_NAME = "abstract_class_py.jinja2"

_PYTHON_ATTRIBUTES_IMPLEMENTATIONS_DIR_PATH = "./attribute_system/attributes_implementations/python"
_PYTHON_SUPPORT_SCRIPTS_IMPLEMENTATIONS_DIR_PATH = "./class_desc_gen/plugins/python_autogen/scripts"

_TARGET_LANGUAGE = "python"

_STATIC_VAR_ATTRIBUTE_NAME = "static"
_CONST_VAR_ATTRIBUTE_NAME = "const"

_JINJA_PROPERTY = namedtuple("_JINJA_PROPERTY", ["name", "val", "const"])


def _collect_all_class_attrs_functions(abstract_class: AbstractClass) -> Tuple[List[Tuple[Callable, str]], List[Callable]]:
    class_attrs_autogen_functions = []
    class_attrs_import_function = []
    for class_attr in abstract_class.attrs:
        class_attrs_autogen_functions.append((get_attribute_autogen_function(attribute_name=class_attr.name,
                                                                             target_lan=_TARGET_LANGUAGE),
                                              class_attr.name))
        class_attrs_import_function.append(get_attribute_import_function(attribute_name=class_attr.name,
                                                                         target_lan=_TARGET_LANGUAGE))

    for cur_prop in abstract_class.properties:
        for attr in cur_prop.attrs:
            attr_options = get_attribute_options(attribute_name=attr.name, target_lan=_TARGET_LANGUAGE)
            if attr_options["is_class_attribute"]:
                class_attrs_autogen_functions.append((get_attribute_autogen_function(attribute_name=attr.name,
                                                                                     target_lan=_TARGET_LANGUAGE),
                                                      attr.name))
                class_attrs_import_function.append(get_attribute_import_function(attribute_name=attr.name,
                                                                                 target_lan=_TARGET_LANGUAGE))

    return class_attrs_autogen_functions, class_attrs_import_function


def _collect_properties_names(abstract_class: AbstractClass) -> List[str]:
    return [prop.name for prop in abstract_class.properties]


def _collect_properties_types(abstract_class: AbstractClass) -> Dict:
    res = dict()
    for prop in abstract_class.properties:
        res[prop.name] = prop.type
    return res


def _collect_properties_attributes(abstract_class: AbstractClass) -> Dict:
    res = {}
    for prop in abstract_class.properties:
        cur_attrs = dict()
        for attr in prop.attrs:
            cur_attrs[attr.name] = str(attr.val)
        res[prop.name] = cur_attrs
    return res


def _collect_properties_with_static_flag(abstract_class: AbstractClass, static_flag: bool) -> List[_JINJA_PROPERTY]:
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
        res.append(_JINJA_PROPERTY(name=prop.name, val=val, const=is_const))
    return res


def _collect_static_properties(abstract_class: AbstractClass) -> List[_JINJA_PROPERTY]:
    return _collect_properties_with_static_flag(abstract_class=abstract_class, static_flag=True)


def _collect_properties(abstract_class: AbstractClass) -> List[_JINJA_PROPERTY]:
    return _collect_properties_with_static_flag(abstract_class=abstract_class, static_flag=False)


def _print_method(abstract_method: AbstractMethod) -> str:
    method_name_str = "    def %s(self, " % abstract_method.name
    method_params_str = ''.join(["%s: %s, " % (param.name, get_language_type(param.type, _TARGET_LANGUAGE)) for param in abstract_method.params])
    if not method_params_str:
        method_name_str = method_name_str[:-2]
    method_params_str = (method_params_str[:-2] if method_params_str else "") + ")"
    method_out_str = ":\n"
    if abstract_method.return_type:
        method_out_str = " -> %s" % get_language_type(abstract_method.return_type, _TARGET_LANGUAGE) + method_out_str
    method_body_str = "        pass\n"
    return method_name_str + method_params_str + method_out_str + method_body_str


def _create_init_script_in_directory(dir_path: str):
    with open(os.path.join(dir_path, "__init__.py"), "w") as f:
        f.write("")


def _print_all_class_methods(abstract_class: AbstractClass) -> str:
    return ''.join(["%s\n" % _print_method(method) for method in abstract_class.methods])


class PythonAutoGenPlugin(object):
    def __init__(self, plugin_desc_params: _PluginParams):
        self.params = plugin_desc_params

    def run(self, abstract_class: AbstractClass, output_dir_name: str, dsc_file_name: str):
        if os.path.exists(output_dir_name):
            shutil.rmtree(output_dir_name)
        if not os.path.exists(output_dir_name):
            os.mkdir(output_dir_name)

        # ##################### #
        # JINJA2 initialization #
        # ##################### #

        jinja_env = Environment(loader=FileSystemLoader(_JINJA_TEMPLATES_DIR_PATH))
        desc_class_template = jinja_env.get_template(_JINJA_DESC_CLASS_TEMPLATE_NAME)
        abstract_class_template = jinja_env.get_template(_JINJA_ABSTRACT_CLASS_TEMPLATE_NAME)

        # ###################################### #
        # Support variables for jinja2 rendering #
        # ###################################### #

        properties_names = _collect_properties_names(abstract_class=abstract_class)
        properties_types = _collect_properties_types(abstract_class=abstract_class)
        properties_attributes = _collect_properties_attributes(abstract_class=abstract_class)

        class_static_properties = _collect_static_properties(abstract_class=abstract_class)
        class_properties = _collect_properties(abstract_class=abstract_class)

        class_attrs_autogen_functions, class_attrs_import_functions = _collect_all_class_attrs_functions(abstract_class)
        partial_attrs_autogen_functions = []
        for func, attr_name in class_attrs_autogen_functions:
            partial_func = partial(func, abstract_class=abstract_class)
            partial_func.__name__ = "Autogen function for attribute '%s'" % attr_name
            partial_attrs_autogen_functions.append(partial_func)

        partial_methods_print_func = partial(_print_all_class_methods, abstract_class=abstract_class)

        # ############################ #
        # Render Abstract Class Script #
        # ############################ #

        rendered = abstract_class_template.render(class_name_camel_case=abstract_class.name,
                                                  properties_names=properties_names,
                                                  properties_types=properties_types,
                                                  properties_attributes=properties_attributes)
        abstract_class_dir_path = os.path.join(output_dir_name, "abstract_class")
        shutil.copytree(_PYTHON_SUPPORT_SCRIPTS_IMPLEMENTATIONS_DIR_PATH, abstract_class_dir_path)
        _create_init_script_in_directory(abstract_class_dir_path)
        with open(os.path.join(abstract_class_dir_path, "abstract_class.py"), "w") as f:
            f.write(rendered)

        # ######################## #
        # Render Desc Class Script #
        # ######################## #

        rendered = desc_class_template.render(class_attrs_autogen_functions=partial_attrs_autogen_functions,
                                              class_attrs_import_functions=class_attrs_import_functions,
                                              class_name_camel_case=abstract_class.name,
                                              class_static_properties=class_static_properties,
                                              class_properties=class_properties,
                                              class_methods_print_func=partial_methods_print_func)

        autogen_file_path = os.path.join(output_dir_name, dsc_file_name + ".py")
        with open(autogen_file_path, "w") as f:
            f.write(rendered)

        attributes_impls_dir = os.path.join(output_dir_name, "attributes")
        shutil.copytree(_PYTHON_ATTRIBUTES_IMPLEMENTATIONS_DIR_PATH, attributes_impls_dir)
        _create_init_script_in_directory(attributes_impls_dir)
