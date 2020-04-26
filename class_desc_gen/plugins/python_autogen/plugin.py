import os
import shutil

from functools import partial
from jinja2 import Environment, FileSystemLoader

from abstract_class.absract_class import AbstractClass, AbstractMethod
from class_desc_gen._config_parser import _PluginParams
from class_desc_gen.types_converter import get_language_type
from class_desc_gen.plugins import collect_properties_attributes, collect_properties_types, collect_properties_names
from class_desc_gen.plugins import collect_properties, collect_static_properties
from class_desc_gen.plugins import collect_all_class_attrs_functions


_JINJA_TEMPLATES_DIR_PATH = "./class_desc_gen/plugins/python_autogen/templates"
_JINJA_DESC_CLASS_TEMPLATE_NAME = "desc_class_py.jinja2"
_JINJA_ABSTRACT_CLASS_TEMPLATE_NAME = "abstract_class_py.jinja2"

_PYTHON_ATTRIBUTES_IMPLEMENTATIONS_DIR_PATH = "./attribute_system/attributes_implementations/python"
_PYTHON_SUPPORT_SCRIPTS_IMPLEMENTATIONS_DIR_PATH = "./class_desc_gen/plugins/python_autogen/scripts"

_TARGET_LANGUAGE = "python"


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

        properties_names = collect_properties_names(abstract_class=abstract_class)
        properties_types = collect_properties_types(abstract_class=abstract_class)
        properties_attributes = collect_properties_attributes(abstract_class=abstract_class)

        class_static_properties = collect_static_properties(abstract_class=abstract_class, target_lan=_TARGET_LANGUAGE)
        class_properties = collect_properties(abstract_class=abstract_class, target_lan=_TARGET_LANGUAGE)

        class_attrs_autogen_functions, class_attrs_import_functions = collect_all_class_attrs_functions(abstract_class, _TARGET_LANGUAGE)
        partial_attrs_autogen_functions = []
        for func, attr_name in class_attrs_autogen_functions:
            if func is None:
                continue

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
