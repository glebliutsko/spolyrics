from time import sleep

import requests
from PyQt5.QtCore import QThread, pyqtSignal, QWaitCondition, QMutex

import constants
from spotify import SpotifyAPI, OAuthPKCE, Track


class TrackLyrics:
    track: Track
    lyrics: str


class SpotifyUpdater(QThread):
    authorization_required = pyqtSignal(str)
    track_changed = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(SpotifyUpdater, self).__init__(*args, **kwargs)

        oauth = OAuthPKCE(constants.Spotify.CLIENT_ID, constants.Spotify.REDIRECT_URL, constants.Spotify.SCOPE)
        self.api = SpotifyAPI(self.auth, 'ru', oauth)

        self.__session = requests.session()

        self.wait_authorization = QWaitCondition()

        # Небольшой хак. После завершения авторизайии, сюда будет записан URL Redirect с кодом.
        self.url_with_code = None

    def auth_complete(self, url):
        self.url_with_code = url

    def auth(self, url: str) -> str:
        self.authorization_required.emit(url)
        # Ожидаем завершения авторизации
        self.wait_authorization.wait(QMutex())
        return self.url_with_code

    def run(self):
        if not self.api.is_auth:
            self.api.auth()

        while True:
            current_track = self.api.get_current_track()
            if current_track is not None:
                self.track_changed.emit(f'Hello World: {current_track}')

            sleep(1)
