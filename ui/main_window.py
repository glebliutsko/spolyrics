from PyQt5.QtWidgets import QMainWindow

from ui.designer.mainwindow import Ui_MainWindow
from ui.web_auth import WebAuth


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.web = WebAuth()
        self.web.show()
