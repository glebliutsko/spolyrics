from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox

import constants
from service import Genius, YandexMusic
from spotify import SpotifyUpdater, OAuthPKCE
from ui.designer.mainwindow import Ui_MainWindow
from ui.web_auth import WebAuth


class MainWindow(QMainWindow):
    auth_complete = pyqtSignal(str)

    SERVICES_TEXT = [Genius, YandexMusic]

    def __init__(self):
        super(QMainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.current_track = None

        for service in self.SERVICES_TEXT:
            self.ui.serviceComboBox.addItem(service.NAME, service)
        self.ui.serviceComboBox.currentIndexChanged.connect(self.change_service)

        self.webauth = WebAuth()

        self.updater = SpotifyUpdater()

        self.auth_complete.connect(self.updater.auth_complete)
        self.updater.authorization_required.connect(self.spotify_authorization_required)
        self.updater.track_changed.connect(self.spotify_track_change)

        self.updater.start()

    def change_service(self, index: int):
        self.update_text()

    def spotify_track_change(self, new_track):
        self.current_track = new_track
        self.update_text()

    def update_text(self):
        if self.current_track is None:
            return

        service = self.ui.serviceComboBox.currentData()()
        text = service.get_text(self.current_track)
        self.ui.lyricsTextEdit.setText(text)

    def spotify_authorization_required(self, url: str):
        def change_url(qurl: QUrl):
            url = qurl.url()

            if url.startswith(constants.Spotify.REDIRECT_URL):
                self.auth_complete.emit(url)
                self.updater.wait_authorization.wakeAll()
                self.webauth.close()

        self.webauth.ui.webEngineView.setUrl(QUrl(url))
        self.webauth.show()

        self.webauth.ui.webEngineView.urlChanged.connect(change_url)
