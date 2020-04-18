import os
import json

_VAR_NOT_SERIALIZABLE_ATTR_NAME = "not_serializable"
_VAR_CONST_SERIALIZABLE_ATTR_NAME = "const"


class JsonException(Exception):
    pass


def json_serializable_class_attribute(class_to_dec):
    def save_to_json(self, path_to_save):
        dict_to_save = dict()
        for prop_name in self._abstract_class.iter_properties_names():
            if self._abstract_class.has_prop_attribute(prop_name, _VAR_NOT_SERIALIZABLE_ATTR_NAME) or\
               self._abstract_class.has_prop_attribute(prop_name, _VAR_CONST_SERIALIZABLE_ATTR_NAME):
                continue

            dict_to_save[prop_name] = str(getattr(self, prop_name))

        with open(path_to_save, "w") as f:
            json.dump(dict_to_save, f, indent=4)

    setattr(class_to_dec, 'save_to_json', save_to_json)
    return class_to_dec


def json_deserializable_class_attribute(class_to_dec):
    def load_from_json(self, path_to_load_from):
        if not os.path.exists(path_to_load_from):
            raise JsonException("Path to load from is invalid. File '%s' doesn't exist." % path_to_load_from)

        with open(path_to_load_from, "r") as f:
            data_from_file = json.load(f)

        for prop_name in self._abstract_class.iter_properties_names():
            cur_prop_built_in_type = self._abstract_class.get_property_built_in_type(prop_name)
            if self._abstract_class.has_prop_attribute(prop_name, _VAR_CONST_SERIALIZABLE_ATTR_NAME):
                continue

            if self._abstract_class.has_prop_attribute(prop_name, _VAR_NOT_SERIALIZABLE_ATTR_NAME):
                setattr(self, prop_name, cur_prop_built_in_type())
            else:
                setattr(self, prop_name, cur_prop_built_in_type(data_from_file[prop_name]))

    setattr(class_to_dec, 'load_from_json', load_from_json)
    return class_to_dec
