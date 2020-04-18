def json_serializable_import_function():
    return "from .attributes.json_attr import json_serializable_class_attribute"


def json_deserializable_import_function():
    return "from .attributes.json_attr import json_deserializable_class_attribute"


def category_import_function():
    return "from .attributes.category_attr import category_class_attribute"


def sorted_import_function():
    return "from .attributes.sorted_attr import sorted_class_attribute"
