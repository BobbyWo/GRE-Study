from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Communicate(QObject):
    changed = pyqtSignal()

class MyMovableWidget(QLabel):
    """WToolBar is a personalized toolbar."""

    homeAction = None

    oldPos = QPoint()
    embbed_answer_box = -1
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
        self.posChanged.emit(self.get_changed_pos())

    def showEvent(self, evt):
        self.original_pos = self.pos()

    def return_original_pos(self):
        self.move(self.original_pos)
    def get_changed_pos(self):
        return [self.pos(),self]
    def get_pos(self):
        return self.pos()

    def get_embbed_answer_box(self):
        return self.embbed_answer_box
    def embbed_to_answer_box(self,answer_box_index):
        self.embbed_answer_box = answer_box_index

    def remove_from_answer_box(self):
        self.embbed_answer_box = -1