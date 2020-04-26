import os
import yaml

from functools import wraps


class _AutogenScriptsConfig(object):
    CONFIG = dict()


_AUTOGEN_SCRIPTS_CONFIG_FILE_PATH = "./attribute_system/all_supported_attributes_config.yaml"


def _config_preload(func_to_dec):
    if not _AutogenScriptsConfig.CONFIG:
        with open(_AUTOGEN_SCRIPTS_CONFIG_FILE_PATH, "r") as f:
            _AutogenScriptsConfig.CONFIG = yaml.load(f, Loader=yaml.FullLoader)

    @wraps(func_to_dec)
    def inner(*args, **kwargs):
        return func_to_dec(*args, **kwargs)

    return inner


@_config_preload
def get_attribute_options(attribute_name, target_lan):
    return _AutogenScriptsConfig.CONFIG["attributes"][attribute_name][target_lan]


def _get_attribute_function_by_type(attribute_name, target_lan, function_type):
    attribute_options = get_attribute_options(attribute_name, target_lan)
    key = "%s_function" % function_type
    if attribute_options is None or key not in attribute_options.keys():
        return None
    function_module_path, _function_name = os.path.splitext(attribute_options[key])
    function_name = _function_name[1:]
    function_module = __import__(function_module_path, fromlist=[function_name])
    return getattr(function_module, function_name)


@_config_preload
def get_attribute_autogen_function(attribute_name, target_lan):
    return _get_attribute_function_by_type(attribute_name=attribute_name,
                                           target_lan=target_lan,
                                           function_type="autogen")


@_config_preload
def get_attribute_import_function(attribute_name, target_lan):
    return _get_attribute_function_by_type(attribute_name=attribute_name,
                                           target_lan=target_lan,
                                           function_type="import")
