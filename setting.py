from configparser import ConfigParser
import os
from typing import Optional
from utils import SingletonMeta

# TODO: Путь для Windows и MacOS
# DEFAULT_CONFIG_FILE = os.path.join(os.getenv('HOME'), 'config/spolyrics/config.ini')
DEFAULT_CONFIG_FILE = './config.ini'


class Setting(metaclass=SingletonMeta):
    DEFAULT_CONFIG = {
        'base': {
            'version_config': '1.0',
            'priority_service': ['']
        },
        'spotify': {
            'token': '',
            'expires': '',
            'refresh_token': ''
        }
    }

    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        if self.config_file is None:
            self.config_file = DEFAULT_CONFIG_FILE

        self.__configs = ConfigParser()
        if os.path.isdir(self.config_file):
            raise IsADirectoryError(f'{self.config_file} is a directory, not file')
        elif os.path.isfile(self.config_file):
            self.__configs.read(self.config_file)
        else:
            self._create_default_config()

    def _create_default_config(self):
        self.__configs.read_dict(self.DEFAULT_CONFIG)
        self.save()

    def save(self):
        with open(self.config_file, 'w') as f:
            self.__configs.write(f)
