"""
Config parses's implementation module.
"""

import os
import six
import yaml
import jsonschema

from typing import List

from abstract_class.absract_class import AbstractClass


class _PluginParams(object):
    _SCHEMA = {
        "type": "object",
        "properties": {
            "description": {"type": "string"},
            "clazz": {"type": "string"},
            "output_dir_name": {"type": "string"},
            "enable": {"type": "boolean"},
        }
    }

    def __init__(self, params_dict: dict):
        jsonschema.validate(params_dict, _PluginParams._SCHEMA)
        self.description = params_dict["description"]
        self.clazz_path = params_dict["clazz"]
        self.output_dir_name = params_dict["output_dir_name"]
        self.enable = True if params_dict["enable"] else False


class PluginDesc(object):
    def __init__(self, name: str, data: dict):
        self.name = name
        self.params = _PluginParams(data)
        self.plugin_inst = None

    def load_plugin(self):
        plugin_module_path, _plugin_class_name = os.path.splitext(self.params.clazz_path)
        plugin_class_name = _plugin_class_name[1:]

        plugin_module = __import__(plugin_module_path, fromlist=[plugin_class_name])
        self.plugin_inst = plugin_module.__dict__[plugin_class_name](self.params)

    def run_plugin(self, abstract_class: AbstractClass, output_dir_name: str, dsc_file_name: str):
        self.plugin_inst.run(abstract_class=abstract_class,
                             output_dir_name=os.path.join(output_dir_name, self.params.output_dir_name),
                             dsc_file_name=dsc_file_name)


class ConfigData(object):
    def __init__(self):
        self.supported_languages: List[str] = []
        self.plugins_descs: List[PluginDesc] = []


class ConfigParser(object):
    @staticmethod
    def parse(config_file_path: str) -> ConfigData:
        with open(config_file_path, "r") as f:
            data = yaml.load(f)

        res = ConfigData()
        res.supported_languages = data["supported_languages"]
        res.plugins_descs = [PluginDesc(plugin_name, plugin_data) for plugin_name, plugin_data in six.iteritems(data["plugins"])]
        res.plugins_descs = list(filter(lambda plugin_desc: plugin_desc.params.enable is True, res.plugins_descs))
        for plugin in res.plugins_descs:
            plugin.load_plugin()

        return res
