import configparser
import os
import logging

_log = logging.getLogger("katcpcli")


def default_config():
    config = configparser.ConfigParser()
    config.add_section('favorites')
    return config


def from_file(path):
    _log.debug('Reading config from file: %s', path)

    config = default_config()
    if not os.path.isfile(path):
        _log.debug("No such file: %s", path)
        return config

    try:
        config.read([path])
    except configparser.Error as E:
        _log.error("Cannot parse config file: %s", E)

    return config

