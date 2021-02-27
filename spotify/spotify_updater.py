from time import sleep
from typing import TYPE_CHECKING

import requests
from PyQt5.QtCore import QThread, pyqtSignal, QWaitCondition

import constants
from spotify import SpotifyAPI, OAuthPKCE, Track
from utils import WaitingData

if TYPE_CHECKING:
    from main import Application


class TrackLyrics:
    track: Track
    lyrics: str


class SpotifyUpdater(QThread):
    authorization_required = pyqtSignal(WaitingData, str, str)
    track_changed = pyqtSignal(str)

    def __init__(self, app: 'Application', *args, **kwargs):
        super(SpotifyUpdater, self).__init__(*args, **kwargs)
        self.app = app

        oauth = OAuthPKCE(constants.Spotify.CLIENT_ID, constants.Spotify.REDIRECT_URL, constants.Spotify.SCOPE)
        self.api = SpotifyAPI('ru', oauth) # TODO: Выбор языка системы.

        self.__session = requests.session()

        self.wait_authorization = QWaitCondition()

    def auth(self, url: str) -> str:
        wd = WaitingData()
        self.authorization_required.emit(wd, url, constants.Spotify.REDIRECT_URL)

        wd.wait()
        return wd.get_data()[0]

    def run(self):
        if not self.api.is_auth:
            self.api.auth(self.auth)

        while True:
            current_track = self.api.get_current_track()
            print(current_track)
            if current_track is not None:
                self.track_changed.emit(f'Hello World: {current_track}')

            sleep(int(self.app.config.update_timeout))
