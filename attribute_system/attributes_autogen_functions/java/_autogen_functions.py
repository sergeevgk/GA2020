from jinja2 import Environment, FileSystemLoader, Template
from functools import wraps

from abstract_class.absract_class import AbstractClass

_CONST_VAR_ATTRIBUTE_NAME = "const"
_NOT_SERIALIZABLE_VAR_ATTRIBUTE_NAME = "not_serializable"
_STATIC_VAR_ATTRIBUTE_NAME = "static"
_CATEGORY_CLASS_ATTRIBUTE_NAME = "category"

_JINJA_TEMPLATES_DIR_PATH = "./attribute_system/attributes_autogen_functions/java/templates"
_JINJA_JSON_SER_TEMPLATE = "json_serializable_autogen_java.jinja2"
_JINJA_JSON_DESER_TEMPLATE = "json_deserializable_autogen_java.jinja2"
_JINJA_CATEGORY_TEMPLATE = "category_autogen_java.jinja2"


class _JavaAutogenFunctionsJinja(object):
    ENV: Environment = None
    JSON_SER_TEMPLATE: Template = None
    JSON_DESER_TEMPLATE: Template = None
    CATEGORY_TEMPLATE: Template = None


def _jinja2_preload(func_to_dec):
    if not _JavaAutogenFunctionsJinja.ENV:
        _JavaAutogenFunctionsJinja.ENV = Environment(loader=FileSystemLoader(_JINJA_TEMPLATES_DIR_PATH))
        _JavaAutogenFunctionsJinja.JSON_SER_TEMPLATE = _JavaAutogenFunctionsJinja.ENV.get_template(_JINJA_JSON_SER_TEMPLATE)
        _JavaAutogenFunctionsJinja.JSON_DESER_TEMPLATE = _JavaAutogenFunctionsJinja.ENV.get_template(_JINJA_JSON_DESER_TEMPLATE)
        _JavaAutogenFunctionsJinja.CATEGORY_TEMPLATE = _JavaAutogenFunctionsJinja.ENV.get_template(_JINJA_CATEGORY_TEMPLATE)

    @wraps(func_to_dec)
    def inner(*args, **kwargs):
        return func_to_dec(*args, **kwargs)

    return inner


def _from_underscore_to_camel_case(string: str) -> str:
    return ''.join(x.capitalize() or '_' for x in string.split('_'))


@_jinja2_preload
def json_serializable_function(abstract_class: AbstractClass):
    return _JavaAutogenFunctionsJinja.JSON_SER_TEMPLATE.render()


@_jinja2_preload
def json_deserializable_function(abstract_class: AbstractClass):
    def get_prop_name(prop):
        prop_name_camel_case = _from_underscore_to_camel_case(prop.name)
        prop_name_camel_case_f_l = prop_name_camel_case[0].lower() + prop_name_camel_case[1:]
        return prop_name_camel_case_f_l

    def filter_prop(prop):
        attrs_names = [attr.name for attr in prop.attrs]
        return _CONST_VAR_ATTRIBUTE_NAME not in attrs_names and \
               _NOT_SERIALIZABLE_VAR_ATTRIBUTE_NAME not in attrs_names and \
               _STATIC_VAR_ATTRIBUTE_NAME not in attrs_names

    props_to_process = list(filter(filter_prop, abstract_class.properties))
    return _JavaAutogenFunctionsJinja.JSON_DESER_TEMPLATE.render(class_name=abstract_class.name,
                                                                 props=[get_prop_name(prop) for prop in props_to_process])


@_jinja2_preload
def category_function(abstract_class: AbstractClass):
    category_name = ""
    for attr in abstract_class.attrs:
        if attr.name == _CATEGORY_CLASS_ATTRIBUTE_NAME:
            category_name = '"%s"' % attr.val
            break
    return _JavaAutogenFunctionsJinja.CATEGORY_TEMPLATE.render(category_name=category_name)
