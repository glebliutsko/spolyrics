from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWidgets import QMainWindow

import constants
from spotify import SpotifyUpdater, OAuthPKCE
from ui.designer.mainwindow import Ui_MainWindow
from ui.web_auth import WebAuth


class MainWindow(QMainWindow):
    auth_complete = pyqtSignal(str)

    def __init__(self):
        super(QMainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.lyricsTextEdit.setReadOnly(False)

        self.webauth = WebAuth()

        oauth = OAuthPKCE(constants.Spotify.CLIENT_ID, constants.Spotify.REDIRECT_URL, constants.Spotify.SCOPE)
        self.updater = SpotifyUpdater(oauth)

        self.auth_complete.connect(self.updater.auth_complete)
        self.updater.need_auth.connect(self.spotify_need_authorization)

        self.updater.start()

    def spotify_track_change(self, new_track):
        pass

    def spotify_need_authorization(self, url: str):
        def change_url(qurl: QUrl):
            url = qurl.url()

            if url.startswith(constants.Spotify.REDIRECT_URL):
                self.auth_complete.emit(url)
                self.updater.conn.wakeAll()
                self.webauth.close()

        self.webauth.ui.webEngineView.setUrl(QUrl(url))
        self.webauth.show()

        self.webauth.ui.webEngineView.urlChanged.connect(change_url)
