import re

from typing import List


class AbstractAttribute(object):
    def __init__(self, name: str='', val=None):
        self.name = name
        self.val = val

    @staticmethod
    def is_attr(string: str):
        res = re.match(r'\s*\[\w+\s*(=\s*\w+\s*)?\]', string)

        return res is not None


class AbstractMethodParam(object):
    def __init__(self, param_type: str, param_name: str):
        self.type = param_type
        self.name = param_name


class AbstractMethod(object):
    def __init__(self, name: str='', return_type='', params: List[AbstractMethodParam]=None):
        self.name = name
        self.params: List[AbstractMethodParam] = params or []
        self.return_type = return_type

    @staticmethod
    def is_method(string: str):
        res = re.match(r'\s*\w+\s+\w+\s*\((\s*\w+\s+\w+\s*,?)*\)', string)

        return res is not None


class AbstractProperty(object):
    def __init__(self, prop_type: str, prop_name: str, prop_attrs=None):
        if prop_attrs is None:
            prop_attrs = []

        self.type = prop_type
        self.name = prop_name
        self.attrs: List[AbstractAttribute] = prop_attrs

    @staticmethod
    def is_property(string: str):
        res = re.match(r'\s*\w+\s+\w+', string)

        return res is not None

    def serialize(self):
        pass


class AbstractClass(object):
    def __init__(self,
                 class_name: str='',
                 attrs: List[AbstractAttribute]=None,
                 properties: List[AbstractProperty]=None,
                 methods: List[AbstractMethod]=None):
        self.name = class_name
        self.attrs = attrs or []
        self.properties = properties or []
        self.methods = methods or []

    @staticmethod
    def is_class(string: str):
        res = re.match(r'\s*class\s+\w+', string)

        return res is not None
