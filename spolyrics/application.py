import logging
import signal
import sys
from typing import TYPE_CHECKING

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication

from spolyrics import constants
from spolyrics.services import SpotifyUpdater
from spolyrics.services.lyrics_providers import GeniusProvider, YandexMusicProvider
from spolyrics.ui.main_window import MainWindow
from spolyrics.ui.web_auth import WebAuth

if TYPE_CHECKING:
    from spolyrics.utils import WaitingData


class Application:
    LYRICS_PROVIDERS = [GeniusProvider, YandexMusicProvider]

    def __init__(self):
        self.logger = logging.getLogger(constants.General.NAME)

        self.app = QApplication(sys.argv)

        self.window = MainWindow(self)
        self._webauth = None

        self.updater = SpotifyUpdater(self, self.window.ui.serviceComboBox.currentData()())

        self.updater.authorization_required.connect(self.browser_authorization)
        self.updater.track_changed.connect(self.window.update_track)
        self.updater.status_change.connect(self.window.update_status)
        self.updater.playing_stopped.connect(self.window.clear_data_track)
        self.window.ui.serviceComboBox.currentIndexChanged.connect(
            lambda index: self.updater.change_service(self.LYRICS_PROVIDERS[index]())
        )

        self.logger.debug('Application initialized.')

    @property
    def webauth(self) -> WebAuth:
        if self._webauth is None:
            self._webauth = WebAuth(self)

        return self._webauth

    def browser_authorization(self, signal: 'WaitingData', url: str, redirect_url: str):
        def change_url(qurl: QUrl):
            url = qurl.url()
            self.logger.debug(f'Browser authentication redirect: {url}')

            # Если мы попали на redirect_url, то авторизация пройдена.
            if url.startswith(redirect_url):
                self.logger.info(f'Browser authentication done: {url}')
                signal.wakeup(url)
                self.webauth.ui.webEngineView.urlChanged.disconnect(change_url)
                self.webauth.close()

        self.logger.info(f'Browser authentication begin: {url}')

        self.webauth.ui.webEngineView.setUrl(QUrl.fromUserInput(url))
        self.webauth.ui.webEngineView.urlChanged.connect(change_url)
        self.webauth.exec()

    def run(self):
        self.logger.info('Application launch.')
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.window.show()

        self.updater.start()
        self.app.exec_()
