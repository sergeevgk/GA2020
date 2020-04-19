from abstract_class.absract_class import AbstractClass


def json_serializable_function(abstract_class: AbstractClass):
    return "@json_serializable_class_attribute"


def json_deserializable_function(abstract_class: AbstractClass):
    return "@json_deserializable_class_attribute"


def category_function(abstract_class: AbstractClass):
    for attr in abstract_class.attrs:
        if attr.name == "category":
            category_name = attr.val
            break
    return "@category_class_attribute(name='%s')" % category_name
