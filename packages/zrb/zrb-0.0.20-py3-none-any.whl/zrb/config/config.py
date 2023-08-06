import logging
import os


def get_logging_level():
    logging_level_str = os.getenv('ZRB_LOGGING_LEVEL', 'WARNING').lower()
    logging_level_map = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'warn': logging.WARN,
        'info': logging.INFO,
        'debug': logging.DEBUG,
        'notset': logging.NOTSET,
    }
    if logging_level_str in logging_level_map:
        return logging_level_map[logging_level_str]
    return logging.WARNING


default_shell = os.getenv('ZRB_SHELL', '')
init_scripts = os.getenv('ZRB_INIT_SCRIPTS', '').split(':')
logging_level = get_logging_level()
should_load_builtin = os.getenv('ZRB_SHOULD_LOAD_BUILTIN', '1') != '0'
env_prefix = os.getenv('ZRB_ENV', '')
