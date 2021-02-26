from typing import Callable, List, Optional, NamedTuple

from spotify.api.oauth_pkce import OAuthPKCE
import requests


class Track(NamedTuple):
    title: str
    album: str
    artists: List[str]


class SpotifyAPI:
    API_URL = 'https://api.spotify.com/v1'

    def __init__(self, callback_auth: Callable[[str], str], lang: str, oauth: OAuthPKCE):
        self.oauth = oauth
        self.__session = requests.session()
        self.callback_auth = callback_auth
        self.set_lang(lang)
        self.is_auth = False

    def _set_authorization_header(self, token: str):
        self.__session.headers.update({'Authorization': f'Bearer {token}'})
        self.is_auth = True

    def auth(self):
        token = self.oauth.auth(self.callback_auth)
        self._set_authorization_header(token)

    def set_lang(self, lang: str):
        self.__session.headers.update({'Accept-Language': lang})

    def get_current_track(self) -> Optional[Track]:
        response = self.__session.get(f'{self.API_URL}/me/player/currently-playing')
        if response.status_code == 204:
            return None

        response = response.json()
        album = response['item']['album']['name']
        artists = [i['name'] for i in response['item']['artists']]
        title = response['item']['name']

        return Track(title, album, artists)
