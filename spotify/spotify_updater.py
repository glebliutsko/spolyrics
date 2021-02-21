from PyQt5.QtCore import QThread, pyqtSignal, QWaitCondition, QMutex

from spotify import OAuthPKCE
import requests

class SpotifyUpdater(QThread):
    SPOTIFY_API = ''

    need_auth = pyqtSignal(str)

    def __init__(self, oauth: OAuthPKCE, *args, **kwargs):
        super(SpotifyUpdater, self).__init__(*args, **kwargs)

        self.oauth = oauth
        self.token = None

        self.__session = requests.session()

        self.conn = QWaitCondition()

        # Небольшой хак. После завершения авторизайии, сюда будет записан URL Redirect с кодом.
        self.url_with_code = None

    def auth_complete(self, url):
        self.url_with_code = url

    def auth(self):
        def callback(url: str) -> str:
            self.need_auth.emit(url)
            # Ожидаем завершения авторизации
            self.conn.wait(QMutex())
            return self.url_with_code

        self.token = self.oauth.auth(callback)
        self.__session.headers.update({'Authorization': f'Bearer {self.token}'})

    def run(self) -> None:
        if not self.token:
            self.auth()

        while True:
            pass

