import logging
from time import sleep
from typing import TYPE_CHECKING

import requests
from PyQt5.QtCore import QThread, pyqtSignal, QWaitCondition

import constants
from spotify import SpotifyAPI, OAuthPKCE, Track
from utils import WaitingData

if TYPE_CHECKING:
    from main import Application
    from services import ServiceABC


class SpotifyUpdater(QThread):
    authorization_required = pyqtSignal(WaitingData, str, str)
    track_changed = pyqtSignal(Track, str)

    def __init__(self, app: 'Application', service: 'ServiceABC', *args, **kwargs):
        self.logger = logging.getLogger('spolyrics')

        super(SpotifyUpdater, self).__init__(*args, **kwargs)
        self.app = app

        oauth = OAuthPKCE(constants.Spotify.CLIENT_ID, constants.Spotify.REDIRECT_URL, constants.Spotify.SCOPE)
        self.api = SpotifyAPI('ru', oauth) # TODO: Выбор языка системы.

        self.__session = requests.session()

        self.wait_authorization = QWaitCondition()

        self.service = service
        self.current_track = None

    def change_service(self, service: 'ServiceABC'):
        self.logger.debug(f'Change service: {service.__class__}')
        self.service = service
        self.current_track = None

    def auth(self, url: str) -> str:
        wd = WaitingData()
        self.authorization_required.emit(wd, url, constants.Spotify.REDIRECT_URL)

        wd.wait()
        return wd.get_data()[0]

    def run(self):
        if not self.api.is_auth:
            self.api.auth(self.auth)

        self.logger.info('Start loop updater.')
        while True:
            current_track = self.api.get_current_track()
            self.logger.debug(f'Current track: {current_track}')

            if current_track is not None and self.current_track != current_track:
                self.logger.info(f'Update current track: {current_track}')

                self.current_track = current_track

                lyrics = self.service.get_text(current_track)

                self.track_changed.emit(current_track, lyrics)

            sleep(int(self.app.config.update_timeout))
