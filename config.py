import os
from configparser import ConfigParser
from typing import Optional

import constants


class Config():
    DEFAULT_CONFIG = {
        'base': {
            'version_config': '1.0'
        },
        'spotify': {
            'update_timeout': '1',
            'update_method': 'spotify'
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
    def version_config(self) -> str:
        return self.__configs['base']['version_config']

    @property
    def update_method(self):
        return self.__configs['spotify']['update_method']

    @property
    def update_timeout(self):
        return self.__configs['spotify']['update_timeout']

    def _create_default_config(self):
        self.__configs.read_dict(self.DEFAULT_CONFIG)
        self.save()

    def save(self):
        with open(self.config_file, 'w') as f:
            self.__configs.write(f)
