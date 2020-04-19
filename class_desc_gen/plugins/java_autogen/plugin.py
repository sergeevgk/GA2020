import os
import shutil

from functools import partial
from jinja2 import Environment, FileSystemLoader, Template

from abstract_class.absract_class import AbstractClass, AbstractMethod
from class_desc_gen._config_parser import _PluginParams
from class_desc_gen.types_converter import get_language_type
from class_desc_gen.plugins import collect_all_class_attrs_functions
from class_desc_gen.plugins import collect_properties, collect_static_properties
from class_desc_gen.plugins import from_underscore_to_camel_case

_JINJA_TEMPLATES_DIR_PATH = "./class_desc_gen/plugins/java_autogen/templates"
_JINJA_DESC_CLASS_TEMPLATE_NAME = "desc_class_java.jinja2"
_JINJA_METHOD_TEMPLATE_NAME = "method.jinja2"

_TARGET_LANGUAGE = "java"

_JSON_ATTRIBUTES_NAMES = ["json_serializable", "json_deserializable"]

_CONST_VAR_ATTRIBUTE_NAME = "const"
_NOT_SERIALIZABLE_VAR_ATTRIBUTE_NAME = "not_serializable"


def _from_underscore_to_camel_case_f_l(string: str):
    camel_case = from_underscore_to_camel_case(string)
    camel_case_f_l = camel_case[0].lower() + camel_case[1:]
    return camel_case_f_l


def _print_method(jinja_template: Template, abstract_method: AbstractMethod) -> str:
    arguments_str = ""
    for param in abstract_method.params:
        arguments_str += "%s %s," % (get_language_type(param.type, _TARGET_LANGUAGE), _from_underscore_to_camel_case_f_l(param.name))
    arguments_str = arguments_str[:-1]
    return jinja_template.render(return_type=get_language_type(abstract_method.return_type, _TARGET_LANGUAGE),
                                 method_name=_from_underscore_to_camel_case_f_l(abstract_method.name),
                                 arguments=arguments_str)


def _print_all_class_methods(jinja_template: Template, abstract_class: AbstractClass) -> str:
    return ''.join(["%s\n" % _print_method(jinja_template, method) for method in abstract_class.methods])


class JavaAutoGenPlugin(object):
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
        method_template = jinja_env.get_template(_JINJA_METHOD_TEMPLATE_NAME)

        # ###################################### #
        # Support variables for jinja2 rendering #
        # ###################################### #

        class_name_camel_case = abstract_class.name
        class_static_properties = collect_static_properties(abstract_class=abstract_class, target_lan=_TARGET_LANGUAGE)
        class_properties = collect_properties(abstract_class=abstract_class, target_lan=_TARGET_LANGUAGE)

        def filter_ignored_prop(prop):
            attrs_names = [attr.name for attr in prop.attrs]
            return _CONST_VAR_ATTRIBUTE_NAME in attrs_names or _NOT_SERIALIZABLE_VAR_ATTRIBUTE_NAME in attrs_names

        ignore_props_names = [_from_underscore_to_camel_case_f_l(prop.name) for prop in list(filter(filter_ignored_prop, abstract_class.properties))]
        ignore_props_names_str = ""
        for prop in ignore_props_names:
            ignore_props_names_str += '"%s", ' % prop
        ignore_props_names_str = ignore_props_names_str[:-2]

        use_json = any([attr.name in _JSON_ATTRIBUTES_NAMES for attr in abstract_class.attrs]) is not None

        autogen_json_functions, _ = collect_all_class_attrs_functions(abstract_class, _TARGET_LANGUAGE)
        partial_attrs_autogen_functions = []
        for func, attr_name in autogen_json_functions:
            if func is None:
                continue

            partial_func = partial(func, abstract_class=abstract_class)
            partial_func.__name__ = "Autogen function for attribute '%s'" % attr_name
            partial_attrs_autogen_functions.append(partial_func)

        methods_str = _print_all_class_methods(method_template, abstract_class)

        # ######################## #
        # Render Desc Class Script #
        # ######################## #

        rendered = desc_class_template.render(class_name_camel_case=class_name_camel_case,
                                              class_static_properties=class_static_properties,
                                              class_properties=class_properties,
                                              use_json=use_json,
                                              attrs_autogen_functions=partial_attrs_autogen_functions,
                                              ignore_props_names=ignore_props_names_str,
                                              methods_str=methods_str)

        autogen_file_path = os.path.join(output_dir_name, dsc_file_name + ".java")
        with open(autogen_file_path, "w") as f:
            f.write(rendered)
