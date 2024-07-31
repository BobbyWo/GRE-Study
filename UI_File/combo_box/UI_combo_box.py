from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class UI_combo_box(QComboBox):
    popupAboutToBeShown = pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(UI_combo_box, self).showPopup()