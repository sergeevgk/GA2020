import os
import six
import json
import pickle


class JsonException(Exception):
    pass


def json_serializable_class_attribute(class_to_dec):
    def save_to_json(self, path_to_save):
        dict_to_save = dict()
        for attr_name, attr_value in six.iteritems(self.__dict__):
            if not callable(attr_value):
                dict_to_save[attr_name] = pickle.dumps(attr_value)

        with open(path_to_save, "w") as f:
            json.dump(dict_to_save, f, indent=4)

    setattr(class_to_dec, 'save_to_json', save_to_json)


def json_deserializable_class_attribute(class_to_dec):
    def load_from_json(self, path_to_load_from):
        if not os.path.exists(path_to_load_from):
            raise JsonException("Path to load from is invalid. File '%s' doesn't exist." % path_to_load_from)

        with open(path_to_load_from, "r") as f:
            data_from_file = json.load(f)

        for attr_name, attr_value in six.iteritems(self.__dict__):
            self.__dict__[attr_name] = pickle.loads(data_from_file[attr_name])

    setattr(class_to_dec, 'load_from_json', load_from_json)
