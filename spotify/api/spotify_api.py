import logging
from typing import Callable, List, Optional, NamedTuple
from urllib.parse import urljoin

import requests

from spotify.api.oauth_pkce import OAuthPKCE


class Track(NamedTuple):
    id: str
    title: str
    album: str
    artists: List[str]


class SpotifyAPI:
    API_URL = 'https://api.spotify.com/v1/'

    def __init__(self, lang: str, oauth: OAuthPKCE):
        self.logger = logging.getLogger('spolyrics')

        self.oauth = oauth
        self.__session = requests.session()
        self.set_lang(lang)
        self.is_auth = False

    def _set_authorization_header(self, token: str):
        self.logger.debug(f'Set authorization header: Authorization: Bearer {token[:5]}...')
        self.__session.headers.update({'Authorization': f'Bearer {token}'})
        self.is_auth = True

    def auth(self, callback_auth: Callable[[str], str]):
        token = self.oauth.auth(callback_auth)
        self._set_authorization_header(token)

    def set_lang(self, lang: str):
        self.logger.debug(f'Set lang spotify api: {lang}')
        self.__session.headers.update({'Accept-Language': lang})

    def _get(self, endpoint: str, params: Optional[dict] = None) -> Optional[dict]:
        url_endpoint = urljoin(self.API_URL, endpoint)
        if params is None:
            params = {}

        response = self.__session.get(url_endpoint, params=params)
        if response.status_code == 204:
            self.logger.debug(f'Spotify API endpoint "/{endpoint}" return: None')
            return None

        response_json = response.json()
        self.logger.debug(f'Spotify API endpoint "/{endpoint}" return: {response_json}')
        return response_json

    def get_current_track(self) -> Optional[Track]:
        response = self._get('me/player/currently-playing')
        if response is None:
            return None

        id_ = response['item']['id']
        album = response['item']['album']['name']
        artists = [i['name'] for i in response['item']['artists']]
        title = response['item']['name']

        return Track(id_, title, album, artists)
