from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QDialog

from ui.designer.webauth import Ui_Dialog


class WebAuth(QDialog):
    def __init__(self):
        super(WebAuth, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # self.ui.webEngineView.setUrl(url)
        self.ui.webEngineView.urlChanged.connect(self.change_url)

    def change_url(self):
        print(self.ui.webEngineView.url())
