from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Communicate(QObject):
    changed = pyqtSignal()

class MyMovableWidget(QLabel):
    """WToolBar is a personalized toolbar."""

    homeAction = None

    oldPos = QPoint()
    posChanged = pyqtSignal(list)
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 1px solid black;")
        self.c = Communicate()
        self.data = 0

    def get_data(self):
        return self.data
    def set_data(self,data):
        self.data = data

    def mousePressEvent(self, evt):
        """Select the toolbar."""
        self.oldPos = evt.globalPos()
    def mouseMoveEvent(self, evt):
        """Move the toolbar with mouse iteration."""

        delta = QPoint(evt.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = evt.globalPos()

    def mouseReleaseEvent(self,evt):
        self.posChanged.emit(self.print_self_pos())

    def showEvent(self, evt):
        self.original_pos = self.pos()

    def return_original_pos(self):
        self.move(self.original_pos)
    def print_self_pos(self):
        return [self.pos(),self]
