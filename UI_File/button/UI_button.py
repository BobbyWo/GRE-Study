from PyQt5.QtWidgets import *

class UI_button(QPushButton):
    def __init__(self,text):
        super().__init__()
        self.setText(text)
        self.setFixedSize(150,40)