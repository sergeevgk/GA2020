"""
Class desc plugin system implementation.
"""

import os
import shutil

from abstract_class.absract_class import AbstractClass
from class_desc_gen._config_parser import ConfigParser, ConfigData


class ClassDescGenSystem(object):
    _CONFIG_FILE_PATH = "./config.yaml"
    _OUTPUT_AUTOGEN_DIR = "./examples/autogen"

    def __init__(self):
        config_parser = ConfigParser()
        config_data: ConfigData = config_parser.parse(ClassDescGenSystem._CONFIG_FILE_PATH)

        self.supported_languages = config_data.supported_languages
        self.plugin_descs = config_data.plugins_descs

    def is_language_valid(self, language: str):
        return language in self.supported_languages

    def run_plugin_on_abstract_class(self, abstract_class: AbstractClass, dsc_file_path: str, target_lan: str):
        for plugin_desc in self.plugin_descs:
            if plugin_desc.name == target_lan:
                dsc_file_basename = os.path.basename(dsc_file_path)
                dsc_file_name, _ = os.path.splitext(dsc_file_basename)
                output_dir = os.path.join(ClassDescGenSystem._OUTPUT_AUTOGEN_DIR, dsc_file_name)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                shutil.copy(dsc_file_path, os.path.join(output_dir, dsc_file_basename))

                plugin_desc.run_plugin(abstract_class=abstract_class,
                                       output_dir_name=output_dir,
                                       dsc_file_name=dsc_file_name)
