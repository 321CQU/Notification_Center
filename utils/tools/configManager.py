import os

from .singletonType import SingletonType

from configparser import ConfigParser

__all__ = ['ConfigReader', 'BASE_DIR']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class ConfigReader(metaclass=SingletonType):
    def __init__(self):
        self._parser = ConfigParser()
        self._parser.read(os.getcwd() + '/utils/config/basic_config.cfg')

    def get_config(self, section: str, attr: str) -> str:
        return self._parser.get(section, attr)
