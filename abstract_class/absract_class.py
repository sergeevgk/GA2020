import re


class AbstractAttribute(object):

    def __init__(self, string: str):
        pass

    @staticmethod
    def is_property_attr(string : str):
        return False


class AbstractProperty(object):

    def __init__(self, prop_type: str, prop_name: str, prop_attrs=None):
        if prop_attrs is None:
            prop_attrs = []

        self.type = prop_type
        self.name = prop_name
        self.attrs = prop_attrs

    @staticmethod
    def is_property(string : str):
        pass

    def serialize(self):
        pass


class AbstractClass(object):

    def __init__(self, class_name: str, attrs=None, properties=None, methods=None):
        self.name = class_name
        self.attrs = attrs or []
        self.properties = properties or []
        self.methods = methods or []


    @staticmethod
    def is_class(string : str):
        pass
