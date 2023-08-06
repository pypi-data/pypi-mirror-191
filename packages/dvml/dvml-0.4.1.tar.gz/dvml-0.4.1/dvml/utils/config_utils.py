"""
Utility functions to handle configurations
"""


def parse_config(conf, default_conf=None):
    """

    :param conf: config passed by the user
    :param default_conf: default config for a given class/method
    :return: parsed configuration with default values for options when missing
    """
    if conf is None:
        conf = {}

    if default_conf is None:
        default_conf = {}
    parsed_conf = {}

    # First, look for options not present in the default config, and preserve them
    for opt, val in conf.items():
        if opt not in default_conf:
            parsed_conf[opt] = val

    # Then, check all the items present in the default config
    for def_opt, def_val in default_conf.items():
        parsed_conf[def_opt] = conf.get(def_opt, def_val)

    return parsed_conf
