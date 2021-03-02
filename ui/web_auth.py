from typing import TYPE_CHECKING

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog

from ui.designer.webauth import Ui_Dialog

if TYPE_CHECKING:
    from main import Application


class WebAuth(QDialog):
    def __init__(self, app: 'Application'):
        super(WebAuth, self).__init__()
        self.app = app

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
