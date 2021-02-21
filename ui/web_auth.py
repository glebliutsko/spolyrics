from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore

from ui.designer.webauth import Ui_Dialog


class WebAuth(QDialog):
    def __init__(self):
        super(WebAuth, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
