from setting import Setting
from spotify import TokenInfo


class InvalidTokenException(Exception):
    pass


class SaverToken:
    def __init__(self):
        self.config = Setting()

    def get_token(self) -> TokenInfo:
        token_info_dict = self.config.spotify
        # Check fields on empty
        for i in token_info_dict.values():
            if i == '':
                raise InvalidTokenException()

        return TokenInfo.parse_dict(token_info_dict)

    def save_token(self, token_info: TokenInfo):
        self.config.spotify = token_info.to_dict()
        self.config.save()
