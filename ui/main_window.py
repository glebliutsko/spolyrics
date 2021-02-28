import webbrowser
from typing import TYPE_CHECKING, Optional

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from services import Genius, YandexMusic
from ui.designer.mainwindow import Ui_MainWindow

if TYPE_CHECKING:
    from main import Application
    from spotify.api.spotify_api import Track


class MainWindow(QMainWindow):
    auth_complete = pyqtSignal(str)

    SERVICES_TEXT = [Genius, YandexMusic]

    def __init__(self, app: 'Application'):
        super(QMainWindow, self).__init__()
        self.app = app

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # TODO: Проброс настоящей ссылки
        self.url = 'https://example.com/'

        for service in self.SERVICES_TEXT:
            self.ui.serviceComboBox.addItem(service.NAME, service)

        self.ui.nameTrackLabel.mousePressEvent = self.open_link_browser

    def update_track(self, track: 'Track', lyrics: Optional[str], url: Optional[str] = None):
        self.ui.nameTrackLabel.setText(f'{track.artists_str()} - {track.title}')
        if lyrics != '':
            self.ui.lyricsTextEdit.setText(lyrics)
        else:
            self.ui.lyricsTextEdit.setText('Lyrics not found.')

    def open_link_browser(self, *args):
        webbrowser.open(self.url)
