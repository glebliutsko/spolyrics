from typing import TYPE_CHECKING

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from services import Genius, YandexMusic
from ui.designer.mainwindow import Ui_MainWindow

if TYPE_CHECKING:
    from main import Application


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
        self.ui.serviceComboBox.currentIndexChanged.connect(self.update_service)
        self.service = self.ui.serviceComboBox.currentData()

    def update_service(self, *args):
        self.service = self.ui.serviceComboBox.currentData()
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
