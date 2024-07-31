import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
# import PyQt5.QtCore
class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.praticeObject = QStackedWidget()
        question_list = []
        for x in range(5):
            container = QWidget()
            page_layout = QVBoxLayout()
            text_layout = QHBoxLayout()
            button_layout = QHBoxLayout()
            label = QLabel(str(x))
            label.setAlignment(Qt.AlignCenter)
            back_button = QPushButton("Previous page")
            back_button.clicked.connect(lambda checked, x=x: self.PreviousPage(x))
            button = QPushButton("NextPage")
            button.clicked.connect(lambda checked,x=x:self.nextPage(x))
            text_layout.addWidget(label)
            button_layout.addWidget(back_button)
            button_layout.addWidget(button)
            page_layout.addLayout(text_layout)
            page_layout.addLayout(button_layout)
            container.setLayout(page_layout)
            question_list.append(container)
        for y in question_list:
            self.praticeObject.addWidget(y)
        self.setCentralWidget(self.praticeObject)
    def nextPage(self, value):
        self.praticeObject.setCurrentIndex(value+1)

    def PreviousPage(self, value):
        self.praticeObject.setCurrentIndex(value-1)
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())