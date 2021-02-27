import json
import logging
import os

import constants
from spotify import TokenInfo


class TokenNotSave(Exception):
    pass


class SaverToken:
    def __init__(self):
        self.logger = logging.getLogger('spolyrics')

        self.filename = os.path.join(constants.Config.DEFAULT_DIRECTORY_SAVE_AUTH, 'spotify.json')

    def get_token(self) -> TokenInfo:
        if not os.path.exists(self.filename):
            raise TokenNotSave()

        with open(self.filename, 'r') as f:
            self.logger.debug(f'Read cache config from {self.filename}')
            token_info_dict = json.load(f)

        return TokenInfo.parse_dict(token_info_dict)

    def save_token(self, token_info: TokenInfo):
        self.logger.debug(f'Write cache config from {self.filename}')
        with open(self.filename, 'w') as f:
            json.dump(token_info.to_dict(), f)
