import webbrowser
from typing import TYPE_CHECKING, Optional

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from spolyrics.ui.designer.mainwindow import Ui_MainWindow

if TYPE_CHECKING:
    from spolyrics import Application
    from spolyrics.services.spotify.spotify_api import Track
    from spolyrics.services import StatusABC


class MainWindow(QMainWindow):
    auth_complete = pyqtSignal(str)

    def __init__(self, app: 'Application'):
        super(QMainWindow, self).__init__()
        self.app = app

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.url = None

        for service in self.app.LYRICS_PROVIDERS:
            self.ui.serviceComboBox.addItem(service.NAME, service)

        self.ui.nameTrackLabel.mousePressEvent = self.open_link_browser

    def update_status(self, status: 'StatusABC'):
        if status.is_error:
            css_style = 'color: #ff0000'
        else:
            css_style = 'color: #000000'

        self.ui.statusLabel.setStyleSheet(css_style)
        self.ui.statusLabel.setText(str(status))

    def clear_data_track(self):
        self.ui.nameTrackLabel.setText(None)
        self.ui.lyricsTextEdit.setText(None)
        self.url = None

    def update_track(self, track: 'Track', lyrics: Optional[str]):
        self.url = track.url
        self.ui.nameTrackLabel.setText(f'{track.artists_str()} - {track.title}')
        if lyrics != '':
            self.ui.lyricsTextEdit.setText(lyrics)
        else:
            self.ui.lyricsTextEdit.setText('Lyrics not found.')

    def open_link_browser(self, *args):
        if self.url is not None:
            webbrowser.open(self.url)
