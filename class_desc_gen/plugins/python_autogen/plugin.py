import os
import shutil

from functools import partial
from jinja2 import Environment, FileSystemLoader

from abstract_class.absract_class import AbstractClass, AbstractMethod
from class_desc_gen._config_parser import _PluginParams
from class_desc_gen.types_converter import get_language_type
from attribute_system import get_attribute_autogen_function, get_attribute_options, get_attribute_import_function


_JINJA_TEMPLATES_DIR_PATH = "./class_desc_gen/plugins/python_autogen/templates"
_JINJA_SOURCE_CODE_TEMPLATE_NAME = "source_code_py.jinja2"

_PYTHON_ATTRIBUTES_IMPLEMENTATIONS_DIR_PATH = "./attribute_system/attributes_implementations/python"

_TARGET_LANGUAGE = "python"


def _collect_all_class_attrs_functions(abstract_class: AbstractClass):
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


def _collect_properties_names(abstract_class: AbstractClass):
    return [prop.name for prop in abstract_class.properties]


def _print_method(abstract_method: AbstractMethod):
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


def _print_all_class_methods(abstract_class: AbstractClass):
    return ''.join(["%s\n" % _print_method(method) for method in abstract_class.methods])


class PythonAutoGenPlugin(object):
    def __init__(self, plugin_desc_params: _PluginParams):
        self.params = plugin_desc_params

    def run(self, abstract_class: AbstractClass, output_dir_name: str, dsc_file_name: str):
        if not os.path.exists(output_dir_name):
            os.mkdir(output_dir_name)

        jinja_env = Environment(loader=FileSystemLoader(_JINJA_TEMPLATES_DIR_PATH))
        source_code_template = jinja_env.get_template(_JINJA_SOURCE_CODE_TEMPLATE_NAME)

        class_attrs_autogen_functions, class_attrs_import_functions = _collect_all_class_attrs_functions(abstract_class)
        partial_attrs_autogen_functions = []
        for func, attr_name in class_attrs_autogen_functions:
            partial_func = partial(func, abstract_class=abstract_class)
            partial_func.__name__ = "Autogen function for attribute '%s'" % attr_name
            partial_attrs_autogen_functions.append(partial_func)

        properties_names = _collect_properties_names(abstract_class=abstract_class)

        partial_methods_print_func = partial(_print_all_class_methods, abstract_class=abstract_class)

        rendered = source_code_template.render(class_attrs_autogen_functions=partial_attrs_autogen_functions,
                                               class_attrs_import_functions=class_attrs_import_functions,
                                               class_name=abstract_class.name,
                                               class_properties_names=properties_names,
                                               class_methods_print_func=partial_methods_print_func)

        autogen_file_path = os.path.join(output_dir_name, dsc_file_name + ".py")
        with open(autogen_file_path, "w") as f:
            f.write(rendered)

        attributes_impls_dir = os.path.join(output_dir_name, "attributes")
        if os.path.exists(attributes_impls_dir):
            shutil.rmtree(attributes_impls_dir)
        shutil.copytree(_PYTHON_ATTRIBUTES_IMPLEMENTATIONS_DIR_PATH, attributes_impls_dir)
