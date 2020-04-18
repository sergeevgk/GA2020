import six

from typing import Dict, Type

from .types import Types
from .types import from_string_to_custom_type, from_custom_type_to_built_in_type


class AbstractPersonClass(object):
    """
    Abstract class for python class Person.
    It's private fields:
        __properties_fields_names__ : List[str]    - list of properties' names
        __properties_types_str__    : Dict         - list of properties' types' names
        __properties_types__        : List[Type]   - list of properties' types as built in classes
        __properties_attributes__   : Dict         - dictionary of properties' attributes' names and its values

    It's protected methods:
        get_property_attributes(prop_name)    -> Dict
        get_property_custom_type(prop_name)   -> Types
        get_property_built_in_type(prop_name) -> Type
    """

    __properties_fields_names__ = ['is_man', 'age', 'first_name', 'last_name', 'thirty', 'money_is_not_a_problem', 'class_name', 'ten', 'twelve']
    __properties_types_str__ = {'is_man': 'bool', 'age': 'int', 'first_name': 'str', 'last_name': 'str', 'thirty': 'int', 'money_is_not_a_problem': 'bool', 'class_name': 'str', 'ten': 'int', 'twelve': 'int'}
    __properties_types__ = {prop_name:from_string_to_custom_type(prop_type) for prop_name, prop_type in six.iteritems(__properties_types_str__)}
    __properties_attributes__ = {'is_man': {}, 'age': {}, 'first_name': {}, 'last_name': {}, 'thirty': {'const': '30'}, 'money_is_not_a_problem': {'not_serializable': 'None'}, 'class_name': {'not_serializable': 'None', 'static': 'None', 'const': 'Person'}, 'ten': {'static': 'None', 'const': '10'}, 'twelve': {'static': 'None'}}

    def iter_properties_names(self):
        for prop_name in self.__properties_fields_names__:
            yield prop_name

    def has_prop_attribute(self, prop_name: str, attr_name: str) -> bool:
        return attr_name in self.get_property_attributes(prop_name).keys()

    def get_property_attributes(self, prop_name: str) -> Dict:
        return self.__properties_attributes__[prop_name]

    def get_property_custom_type(self, prop_name: str) -> Types:
        return self.__properties_types__[prop_name]

    def get_property_built_in_type(self, prop_name: str) -> Type:
        return from_custom_type_to_built_in_type(self.get_property_custom_type(prop_name))
