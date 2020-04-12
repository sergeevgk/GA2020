def json_serializable_import_function():
    return "from .attributes._json import json_serializable_class_attribute"


def json_deserializable_import_function():
    return "from .attributes._json import json_deserializable_class_attribute"


def category_import_function():
    return "from .attributes._category import category_class_attribute"


def sorted_import_function():
    return "from .attributes._category import sorted_class_attribute"
