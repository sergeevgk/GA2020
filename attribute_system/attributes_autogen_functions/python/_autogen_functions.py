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


def sorted_function(abstract_class: AbstractClass):
    props = abstract_class.properties
    sorted_props_names = []
    for prop in props:
        prop_attrs_names = [attr.name for attr in prop.attrs]
        if "sorted" in prop_attrs_names:
            sorted_props_names.append(prop.name)
    return "@sorted_class_attribute(vars_names=%s)" % str(sorted_props_names)
