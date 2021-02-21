import os
from configparser import ConfigParser
from typing import Optional

import constants
from utils import SingletonMeta


class Setting(metaclass=SingletonMeta):
    DEFAULT_CONFIG = {
        'base': {
            'version_config': '1.0',
            'priority_service': ['genius'],
            'method': 'api'
        },
        'spotify': {
            'token': '',
            'token_type': '',
            'scope': '',
            'expires': '',
            'refresh_token': ''
        }
    }

    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        if self.config_file is None:
            self.config_file = constants.Config.DEFAULT_CONFIG_FILE

        self.__configs = ConfigParser()
        if os.path.isdir(self.config_file):
            raise IsADirectoryError(f'{self.config_file} is a directory, not file')
        elif os.path.isfile(self.config_file):
            self.__configs.read(self.config_file)
        else:
            self._create_default_config()

    @property
    def method(self):
        return self.__configs['base']['method']

    @property
    def version(self) -> str:
        return self.__configs['base']['version_config']

    @property
    def spotify(self) -> dict:
        return dict(self.__configs['spotify'])

    @spotify.setter
    def spotify(self, values: dict):
        self.__configs['spotify'] = values

    def _create_default_config(self):
        self.__configs.read_dict(self.DEFAULT_CONFIG)
        self.save()

    def save(self):
        with open(self.config_file, 'w') as f:
            self.__configs.write(f)
