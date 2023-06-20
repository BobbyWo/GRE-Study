from pprint import pprint

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QPushButton, QGroupBox
import tkinter as tk
from PIL import ImageGrab
import sys
import cv2
import numpy as np
# import imageToString
import pyperclip
import webbrowser
import pytesseract

import cambridge_search
import notion


class Communicate(QObject):
    snip_saved = pyqtSignal()


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.win_width = 650
        self.win_height = 300
        self.setGeometry(50, 50, self.win_width, self.win_height)
        self.setWindowTitle("Snipping Tool for Programmers")
        self.dict_search = cambridge_search.cambridge_search()
        self.notion_call = notion.notion_API()
        self.initUI()

    def initUI(self):
        self.combo = QComboBox(self)
        pages = self.notion_call.get_block_list()
        self.page = dict(pages)
        for key in self.page.keys():
            self.combo.addItem(key)
        self.combo.move(10, 30)
        self.combo.setFixedSize(self.win_width - 20, 20)
        # self.search_browser = self.combo.currentText()

        self.combo.activated[str].connect(self.onChanged)

        self.searchDirlabel = QLabel(self)
        self.searchDirlabel.move(10, 10)
        self.searchDirlabel.setText('Page')
        self.searchDirlabel.adjustSize()

        # Define buttons
        x = 1
        self.I_T_S_Question = QPushButton(self)
        self.I_T_S_Question.setText("Image to String(Question)")
        self.I_T_S_Question.move(int((self.win_width / 4 * (x - 1)) + 10), 75)
        self.I_T_S_Question.setFixedSize(150, 40)
        self.I_T_S_Question.clicked.connect(self.Question_Button_clicked)
        x += 1

        self.I_T_S_Answer = QPushButton(self)
        self.I_T_S_Answer.setText("Image to String(Answer)")
        self.I_T_S_Answer.move(int((self.win_width / 4 * (x - 1)) + 10), 75)
        self.I_T_S_Answer.setFixedSize(150, 40)
        self.I_T_S_Answer.clicked.connect(self.Answer_Button_clicked)
        x += 1

        self.createTable = QPushButton(self)
        self.createTable.setText("Create Table")
        self.createTable.move(int((self.win_width / 4 * (x - 1)) + 10), 75)
        self.createTable.setFixedSize(150, 40)
        self.createTable.clicked.connect(self.CreateTable_Button_clicked)
        x += 1

        self.paraTrans = QPushButton(self)
        self.paraTrans.setText("Paragraph trans")
        self.paraTrans.move(int((self.win_width / 4 * (x - 1)) + 10), 75)
        self.paraTrans.setFixedSize(150, 40)
        self.paraTrans.clicked.connect(self.ParagraphTranslation_Button_clicked)

        self.notificationBox = QGroupBox("Notification Box", self)
        self.notificationBox.move(10, 135)
        self.notificationBox.setFixedSize(self.win_width - 20, 55)

        self.notificationText = QLabel(self)
        self.notificationText.move(20, 145)
        self.reset_notif_text()

    def Question_Button_clicked(self):
        self.snipWin = SnipWidget("I_T_S_Question", self)
        self.snipWin.notification_signal.connect(self.reset_notif_text)
        self.snipWin.show()
        self.notificationText.setText("cap question button clicked")
        self.update_notif()

    def Answer_Button_clicked(self):
        self.snipWin = SnipWidget("I_T_S_Answer", self)
        self.snipWin.notification_signal.connect(self.reset_notif_text)
        self.snipWin.show()
        self.notificationText.setText("cap answer button clicked")
        self.update_notif()

    def CreateTable_Button_clicked(self):
        self.notion_call.create_table()

    def ParagraphTranslation_Button_clicked(self):
        self.snipWin = SnipWidget("paraTrans", self)
        self.snipWin.notification_signal.connect(self.reset_notif_text)
        self.snipWin.show()
        self.notificationText.setText("paragraph translation button clicked")
        self.update_notif()


    def onChanged(self, text):
        temp_text = f'Page changed to {text}. \n'
        self.notificationText.setText(temp_text)
        self.update_notif()
        self.notion_call.change_page(self.page[text])

    def reset_notif_text(self):
        self.notificationText.setText("Idle...")
        self.update_notif()

    def define_notif_text(self, msg):
        print('notification was sent')
        self.notificationText.setText('notification was sent')
        self.update_notif()

    def update_notif(self):
        self.notificationText.move(20, 155)
        self.notificationText.adjustSize()


class SnipWidget(QMainWindow):
    notification_signal = pyqtSignal()

    def __init__(self, type, parent):
        super(SnipWidget, self).__init__()
        self.type = type
        self.parent = parent
        root = tk.Tk()  # instantiates window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        self.is_snipping = False
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.c = Communicate()
        # self.search_browser = search_browser

        self.show()

        if self.type == "I_T_S_Question":
            self.c.snip_saved.connect(self.getQuestion)

        if self.type == "I_T_S_Answer":
            self.c.snip_saved.connect(self.getAnswer)

        if self.type == "paraTrans":
            self.c.snip_saved.connect(self.paraTrans)

    def paintEvent(self, event):
        if self.is_snipping:
            brush_color = (0, 0, 0, 0)
            lw = 0
            opacity = 0
        else:
            brush_color = (128, 128, 255, 128)
            lw = 3
            opacity = 0.3

        self.setWindowOpacity(opacity)
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            print('Quit')
            QtWidgets.QApplication.restoreOverrideCursor();
            self.notification_signal.emit()
            self.close()
        event.accept()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        self.is_snipping = True
        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.is_snipping = False
        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        self.snipped_image = img
        QtWidgets.QApplication.restoreOverrideCursor();
        self.c.snip_saved.emit()
        self.close()
        self.msg = 'snip complete'
        self.notification_signal.emit()

    def getQuestion(self):
        img_str = self.imgToStr(self.snipped_image)
        img_str = img_str.replace("-\n", '')
        img_str = img_str.replace("\n", '')
        self.parent.notion_call.paragraph_content(img_str, type="heading_3")

    def getAnswer(self):
        img_str = self.imgToStr(self.snipped_image)
        self.parent.notion_call.paragraph_content(img_str, type="heading_3")

    def paraTrans(self):
        img_str = self.imgToStr(self.snipped_image)
        words_to_search = img_str.split('\n')[:-1]
        for words in words_to_search:
            definition = self.parent.dict_search.search(words)
            if len(definition) == 0:
                content = [words, "", "", ""]
                self.parent.notion_call.insert_table_row(content)
            words_pos=english_meaning=chinese_meaning=example = ''
            for defi in definition:
                words = dict(defi).get("words")
                pos = dict(defi).get("pos")
                words_pos += words + "\n" + f"({pos})" + '\n\n'
                english_meaning += dict(defi).get("english_meaning") + '\n\n\n'
                chinese_meaning += dict(defi).get("chinese_meaning") + '\n\n\n'
                example += dict(defi).get("example") + '\n\n'
            content = [words_pos, english_meaning, chinese_meaning, example]
            self.parent.notion_call.insert_table_row(content)

    def find_str(self, image_data):

        img = image_data

        h, w = np.shape(img)
        asp_ratio = float(w / h)
        img_width = 500
        img_height = int(round(img_width / asp_ratio))
        desired_image_size = (img_width, img_height)
        img_resized = cv2.resize(img, desired_image_size)
        imgstr = str(pytesseract.image_to_string(img_resized))
        return imgstr

    def imgToStr(self, image):
        img_str = self.find_str(image)
        return img_str


def window():
    app = QApplication(sys.argv)

    win = MyWindow()
    win.show()

    sys.exit(app.exec_())


window()
