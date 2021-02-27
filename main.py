import sys
from typing import TYPE_CHECKING

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication

from config import Config
from spotify import SpotifyUpdater
from ui.main_window import MainWindow
from ui.web_auth import WebAuth

if TYPE_CHECKING:
    from utils import WaitingData


class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.window = MainWindow(self)
        self.webauth = WebAuth(self)
        self.config = Config()

        self.updater = SpotifyUpdater(self)
        self.updater.authorization_required.connect(self.browser_authorization)

    def browser_authorization(self, signal: 'WaitingData', url: str, redirect_url: str):
        def change_url(qurl: QUrl):
            url = qurl.url()

            # Если мы попали на redirect_url, то авторизация пройдена.
            if url.startswith(redirect_url):
                signal.wakeup(url)
                self.webauth.ui.webEngineView.urlChanged.disconnect(change_url)
                self.webauth.close()

        self.webauth.ui.webEngineView.urlChanged.connect(change_url)
        self.webauth.ui.webEngineView.setUrl(QUrl.fromUserInput(url))
        self.webauth.exec()

    def run(self):
        self.window.show()

        self.updater.start()
        self.app.exec()


if __name__ == '__main__':
    app = Application()
    app.run()
