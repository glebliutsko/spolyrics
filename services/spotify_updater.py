import logging
from datetime import datetime
from typing import TYPE_CHECKING

import requests
from PyQt5.QtCore import QThread, pyqtSignal, QWaitCondition

import constants
from exceptions import NetworkError
from services.spotify import SpotifyAPI, OAuthPKCE, Track, OpenerAuthURLABC
from utils import WaitingData

if TYPE_CHECKING:
    from main import Application
    from services.lyrics_providers import LyricsProviderABC


class StatusABC:
    def __init__(self, is_error: bool):
        self.time_update = datetime.now().time()
        self._is_error = is_error

    @property
    def is_error(self) -> bool:
        return self._is_error

    @property
    def short_description(self) -> str:
        raise NotImplemented

    def __str__(self) -> str:
        return f'Update in {self.time_update.strftime("%H:%M:%S")}: {self.short_description}'


class SpotifyPlayingStatus(StatusABC):
    def __init__(self):
        super().__init__(False)

    @property
    def short_description(self) -> str:
        return 'Spotify playing'


class SpotifyNotPlayingStatus(StatusABC):
    def __init__(self):
        super().__init__(True)

    @property
    def short_description(self) -> str:
        return 'Spotify not playing'


class NetworkErrorStatus(StatusABC):
    def __init__(self):
        super().__init__(True)

    @property
    def short_description(self) -> str:
        return 'Network error'


class DifferentTrack:
    def __init__(self, old_track: Track, current_track: Track):
        self.old_track = old_track
        self.current_track = current_track

    @property
    def is_change(self) -> bool:
        return self.old_track != self.current_track

    @property
    def is_playing_track(self) -> bool:
        return self.current_track is not None

    @property
    def is_started_playing_track(self) -> bool:
        return self.old_track is None and self.current_track is not None

    @property
    def is_stopped_playing_track(self) -> bool:
        return self.old_track is not None and self.current_track is None


class QWebEngineOpenerAuthURL(OpenerAuthURLABC):
    def __init__(self, auth_required_signal: pyqtSignal):
        self.auth_required_signal = auth_required_signal

    def open(self, url: str, redirect_url: str) -> str:
        wd = WaitingData()
        self.auth_required_signal.emit(wd, url, redirect_url)

        wd.wait()
        return wd.get_data()[0]


class SpotifyUpdater(QThread):
    authorization_required = pyqtSignal(WaitingData, str, str)
    track_changed = pyqtSignal(Track, str)
    playing_stopped = pyqtSignal()
    status_change = pyqtSignal(StatusABC)

    def __init__(self, app: 'Application', service: 'LyricsProviderABC', *args, **kwargs):
        self.logger = logging.getLogger(constants.General.NAME)

        super(SpotifyUpdater, self).__init__(*args, **kwargs)
        self.app = app

        opener = QWebEngineOpenerAuthURL(self.authorization_required)
        oauth = OAuthPKCE(constants.Spotify.CLIENT_ID,
                          constants.Spotify.REDIRECT_URL,
                          opener,
                          constants.Spotify.SCOPE)
        self.api = SpotifyAPI('ru', oauth)  # TODO: Выбор языка системы.

        self.__session = requests.session()

        self.wait_authorization = QWaitCondition()

        self.service = service
        self.current_track = None

    def change_service(self, service: 'LyricsProviderABC'):
        self.logger.debug(f'Change service: {service.__class__}')
        self.service = service
        self.current_track = None

    def run(self):
        self.logger.info('Start loop updater.')
        while True:
            try:
                current_track = self.api.get_current_track()
                self.logger.debug(f'Current track: {current_track}')
                diff_track = DifferentTrack(self.current_track, current_track)

                if diff_track.is_stopped_playing_track:
                    self.logger.info(f'Spotify stopped playing')
                    self.playing_stopped.emit()
                    self.current_track = current_track
                elif diff_track.is_change:
                    self.logger.info(f'Update current track: {current_track}')

                    lyrics = self.service.get_lyrics(current_track)

                    self.track_changed.emit(current_track, lyrics)
                    self.current_track = current_track

                if diff_track.is_playing_track:
                    self.status_change.emit(SpotifyPlayingStatus())
                else:
                    self.status_change.emit(SpotifyNotPlayingStatus())
            except NetworkError as e:
                self.logger.error(f'Notwork error: {e}')
                self.status_change.emit(NetworkErrorStatus())

            self.sleep(1)
