from typing import TYPE_CHECKING

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

        self.current_track = None

        for service in self.SERVICES_TEXT:
            self.ui.serviceComboBox.addItem(service.NAME, service)

    def update_track(self, track: 'Track', lyrics: str):
        self.ui.nameTrackLabel.setText(f'{track.title} - {track.album}')
        self.ui.lyricsTextEdit.setText(lyrics)
