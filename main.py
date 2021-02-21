import sys

from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow
from spotify import OAuthPKCE


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
    # main()
    oauth = OAuthPKCE('8c2c359638fb440a9f97e771647ffcb6', 'https://open.spotify.com/', ['user-read-playback-state'])
    token = oauth.auth(lambda a: input(f'{a}\nURL: '))
    print(token)
