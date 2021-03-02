import logging
from typing import List, Optional, NamedTuple
from urllib.parse import urljoin

import requests
import requests.exceptions

from exceptions import NetworkError, APIError
from services.spotify import OAuthPKCE


class Track(NamedTuple):
    id: str
    title: str
    album: str
    artists: List[str]

    def artists_str(self):
        return ', '.join(self.artists)

    def __eq__(self, other: Optional['Track']):
        if other is None:
            return False

        return self.id == other.id


class SpotifyAPI:
    API_BASE_URL = 'https://api.spotify.com/v1/'

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

    def _auth(self):
        token = self.oauth.auth()
        self._set_authorization_header(token)

    def set_lang(self, lang: str):
        self.logger.debug(f'Set lang spotify spotify: {lang}')
        self.__session.headers.update({'Accept-Language': lang})

    def _requests(self,
                  method: str,
                  endpoint: str,
                  params: Optional[dict] = None,
                  data: Optional[dict] = None) -> Optional[dict]:
        if not self.is_auth:
            self._auth()

        url_endpoint = urljoin(self.API_BASE_URL, endpoint)

        if params is None:
            params = {}
        if data is None:
            data = {}

        try:
            response = self.__session.request(method, url_endpoint, params=params, data=data, timeout=5)
            response.raise_for_status()
            if response.status_code == 204:
                self.logger.debug(f'Spotify API endpoint "/{endpoint}" return: None')
                return None
        except requests.exceptions.HTTPError as e:
            response = e.response

            if response.status_code == 401:  # 401 обычно возвращиается при истечении токена
                # Обновляем токен и повторяем запрос
                self._auth()
                response = self.__session.request(method, url_endpoint, params=params, data=data)
            else:
                raise APIError(self.__class__, e)
        except requests.exceptions.RequestException as e:
            raise NetworkError(self.__class__, e)

        response_json = response.json()
        self.logger.debug(f'Spotify API endpoint "/{endpoint}" return: {response_json}')
        return response_json

    def get_current_track(self) -> Optional[Track]:
        response = self._requests('GET', 'me/player/currently-playing')
        if response is None:
            return None

        id_ = response['item']['id']
        album = response['item']['album']['name']
        artists = [i['name'] for i in response['item']['artists']]
        title = response['item']['name']

        return Track(id_, title, album, artists)
