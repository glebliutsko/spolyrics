import base64
import hashlib
import logging
import random
import string
from typing import List, Optional
from urllib import parse

import requests
import requests.exceptions

from spolyrics import constants
from spolyrics.exceptions import HTTPError, NetworkError
from spolyrics.services.spotify import TokenInfo, SaverToken, TokenNotSave


class AuthorizeError(Exception):
    pass


class OpenerAuthURLABC:
    def open(self, url: str, redirect_url: str) -> str:
        raise NotImplemented

    def __call__(self, url: str, redirect_url: str) -> str:
        return self.open(url, redirect_url)


class OAuthPKCE:
    ALLOW_CODE_CHARS = string.ascii_letters + string.digits + '_.-~'
    AUTHORIZE_BASE_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_BASE_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id: str, redirect_uri: str, opener: OpenerAuthURLABC, scope: Optional[List[str]] = None):
        self.logger = logging.getLogger(constants.General.NAME)

        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        if self.scope is None:
            self.scope = list()

        self.opener = opener

    @classmethod
    def get_code_verifier(cls) -> str:
        length = random.randint(43, 128)
        code_char = random.choices(cls.ALLOW_CODE_CHARS, k=length)
        return ''.join(code_char)

    def get_code_challenge(self) -> str:
        code_challenge_hash = hashlib.sha256(self.code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge_hash).decode('utf-8')
        return code_challenge.replace('=', '')

    def _generate_codes(self):
        self.code_verifier = self.get_code_verifier()
        self.code_challenge = self.get_code_challenge()

    def _requests(self, method: str, *args, **kwargs) -> requests.Response:
        try:
            response = requests.request(method, *args, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            raise HTTPError(self.__class__, e)
        except requests.exceptions.RequestException as e:
            raise NetworkError(self.__class__, e)

    def get_auth_url(self) -> str:
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'code_challenge_method': 'S256',
            'code_challenge': self.code_challenge,
            'scope': ' '.join(self.scope)
        }

        params_string = parse.urlencode(params)
        return f'{self.AUTHORIZE_BASE_URL}?{params_string}'

    @classmethod
    def parse_response_url(cls, url: str) -> str:
        qs = parse.urlparse(url).query
        qs_parsed = parse.parse_qs(qs)
        if 'error' in qs_parsed:
            raise AuthorizeError(qs_parsed['error'][0])

        return qs_parsed['code'][0]

    def get_access_token(self, code: str) -> TokenInfo:
        data = {
            'client_id': self.client_id,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'code_verifier': self.code_verifier
        }

        response = self._requests('POST', self.TOKEN_BASE_URL, data=data)
        answer = response.json()
        return TokenInfo.parse_response(answer)

    def refresh_token(self, refresh_token: TokenInfo):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token.refresh_token,
            'client_id': self.client_id
        }

        response = self._requests('POST', self.TOKEN_BASE_URL, data=data)
        answer = response.json()
        return TokenInfo.parse_response(answer)

    def auth(self) -> str:
        self._generate_codes()

        saver = SaverToken()
        try:
            token_info = saver.get_token()
            if token_info.is_expired():
                self.logger.info(f'Refresh token: {token_info.token[:5]}...')
                token_info = self.refresh_token(token_info)
                self.logger.info(f'New token: {token_info.token[:5]}...')
                saver.save_token(token_info)
            else:
                self.logger.info(f'Using cached token: {token_info.token[:5]}...')

            return token_info.token
        except TokenNotSave:
            auth_url = self.get_auth_url()
            response_url = self.opener(auth_url, self.redirect_uri)
            code = self.parse_response_url(response_url)
            token_info = self.get_access_token(code)
            self.logger.info(f'New token received: {token_info.token[:5]}')

            saver.save_token(token_info)
            return token_info.token
