import qdarkstyle
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from UI_File.button.UI_button import UI_button


class create_folder_window(QMainWindow):

    file_name = pyqtSignal(str)

    def __init__(self):
        super(create_folder_window, self).__init__()
        self.win_width = 400
        self.horizontal_margin = 20
        self.vertical_margin = 10
        self.setWindowTitle("Create Folder")
        self.init_UI()
    def init_UI(self):
        container = QWidget()
        layout = QVBoxLayout()
        input_bar_layout = self.init_input_bar_layout()
        button_layout = self.init_button_layout()

        layout.addStretch(1)
        layout.addLayout(input_bar_layout)
        layout.addStretch(1)
        layout.addLayout(button_layout)
        layout.addStretch(1)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def init_input_bar_layout(self):
        input_bar_layout = QVBoxLayout()
        input_bar_layout.setContentsMargins(self.horizontal_margin, self.vertical_margin, self.horizontal_margin, 0)

        self.searchWord = QLineEdit()
        self.searchWord.setFixedSize(self.win_width - 20, 20)


        input_bar_layout.addWidget(self.searchWord)
        return input_bar_layout

    def init_button_layout(self):
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(self.horizontal_margin, self.vertical_margin, self.horizontal_margin, 0)
        button_layout.setSpacing(80)
        button_layout.setAlignment(Qt.AlignLeft)

        confirm_button = UI_button("Confirm Create")
        confirm_button.clicked.connect(self.confirm_button_clicked)
        button_layout.addWidget(confirm_button)

        cancel_button = UI_button("Cancel Create")
        cancel_button.clicked.connect(self.cancel_button_clicked)
        button_layout.addWidget(cancel_button)

        return button_layout

    def confirm_button_clicked(self):
        self.file_name.emit(self.searchWord.text())
        self.deleteLater()

    def cancel_button_clicked(self):
        self.deleteLater()

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    w = create_folder_window()
    w.show()

    app.exec_()
