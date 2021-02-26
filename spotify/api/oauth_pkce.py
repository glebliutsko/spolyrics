import base64
import hashlib
import random
import string
from typing import List, Optional, Callable
from urllib import parse

import requests

from spotify import TokenInfo, SaverToken, TokenNotSave


class AuthorizeError(Exception):
    pass


class OAuthPKCE:
    ALLOW_CODE_CHARS = string.ascii_letters + string.digits + '_.-~'
    URL_AUTHORIZE = 'https://accounts.spotify.com/authorize'
    URL_TOKEN = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id: str, redirect_uri: str, scope: Optional[List[str]] = None):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        if self.scope is None:
            self.scope = list()

        self._generate_codes()

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
        return f'{self.URL_AUTHORIZE}?{params_string}'

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

        response = requests.post(self.URL_TOKEN, data=data)
        answer = response.json()
        return TokenInfo.parse_response(answer)

    def auth(self, callback_auth: Callable[[str], str]) -> str:
        saver = SaverToken()
        try:
            token_info = saver.get_token()
            if not token_info.is_expired():
                return token_info.token
        except TokenNotSave:
            pass

        auth_url = self.get_auth_url()
        response_url = callback_auth(auth_url)
        code = self.parse_response_url(response_url)
        token_info = self.get_access_token(code)
        saver.save_token(token_info)
        return token_info.token
