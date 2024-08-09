import qdarkstyle
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from UI_File.button.UI_button import UI_button


class revised_full_chapter_window(QMainWindow):

    revised = pyqtSignal()

    def __init__(self,chapter):
        super(revised_full_chapter_window, self).__init__()
        self.chapter = chapter
        self.win_width = 450
        self.horizontal_margin = 20
        self.vertical_margin = 10
        self.setWindowTitle("Finished Full Chapter")
        self.init_UI()
    def init_UI(self):
        container = QWidget()
        layout = QVBoxLayout()
        input_bar_layout = self.init_announcement_layout()
        button_layout = self.init_button_layout()

        layout.addStretch(1)
        layout.addLayout(input_bar_layout)
        layout.addStretch(2)
        layout.addLayout(button_layout)
        layout.addStretch(1)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def init_announcement_layout(self):
        announcement_layout = QVBoxLayout()
        announcement_layout.setContentsMargins(self.horizontal_margin, self.vertical_margin, self.horizontal_margin, 0)
        announcement_layout.setAlignment(Qt.AlignHCenter)

        self.announcement = QLabel(f"Congraduation!!!, you have completed {self.chapter} review")


        announcement_layout.addWidget(self.announcement)
        return announcement_layout

    def init_button_layout(self):
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(self.horizontal_margin, self.vertical_margin, self.horizontal_margin, 0)
        # button_layout.setSpacing(100)
        button_layout.setAlignment(Qt.AlignCenter)

        confirm_button = UI_button("Review again")
        confirm_button.clicked.connect(self.confirm_button_clicked)
        button_layout.addWidget(confirm_button)

        cancel_button = UI_button("Return")
        cancel_button.clicked.connect(self.cancel_button_clicked)
        button_layout.addWidget(cancel_button)

        return button_layout

    def confirm_button_clicked(self):
        self.revised.emit()
        self.deleteLater()

    def cancel_button_clicked(self):
        self.deleteLater()

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    w = revised_full_chapter_window("test")
    w.show()

    app.exec_()
