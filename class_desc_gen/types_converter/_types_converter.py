import yaml


class _TypesConverterConfig(object):
    CONFIG = dict()


_TYPES_CONVERTER_CONFIG_FILE_PATH = "./class_desc_gen/types_converter/config.yaml"


def _config_preload(func_to_dec):
    if not _TypesConverterConfig.CONFIG:
        with open(_TYPES_CONVERTER_CONFIG_FILE_PATH, "r") as f:
            _TypesConverterConfig.CONFIG = yaml.load(f)

    def inner(*args, **kwargs):
        return func_to_dec(*args, **kwargs)

    return inner


@_config_preload
def get_language_type(type_in_dsc, target_lan):
    return _TypesConverterConfig.CONFIG["types"][target_lan][type_in_dsc]
