from PyQt5.QtWidgets import QDialog

from ui.designer.webauth import Ui_Dialog


class WebAuth(QDialog):
    def __init__(self):
        super(WebAuth, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # self.ui.webEngineView.setUrl(QUrl('https://accounts.spotify.com/ru/authorize?response_type=code&client_id=f4dc97c399124fc99254c5d7ac2bf4bd&redirect_uri=https:%2F%2Fgenify.joshlmao.com%2Fcallback&code_challenge=GB54egJHpv-3bzUBjmgOiWs9rt1KFFdePOoQDZiJtFk&code_challenge_method=S256&state=genify-app&scope=streaming%20user-read-currently-playing%20user-read-playback-state%20user-modify-playback-state%20app-remote-control%20user-read-email%20user-read-private%20user-top-read%20user-read-recently-played'))
        # self.ui.webEngineView.urlChanged.connect(self.change_url)

    def change_url(self):
        print(self.ui.webEngineView.url())
