from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, mouseEvent):
        self.clicked.emit()
