import cv2
import numpy as np
import pytesseract
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import tkinter as tk
from PIL import ImageGrab


class Communicate(QObject):
    snip_saved = pyqtSignal()


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
        self.begin = QPoint()
        self.end = QPoint()
        self.setWindowOpacity(0.3)
        self.is_snipping = False
        QApplication.setOverrideCursor(
            QCursor(Qt.CrossCursor)
        )
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.c = Communicate()

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
        qp = QPainter(self)
        qp.setPen(QPen(QColor('black'), lw))
        qp.setBrush(QColor(*brush_color))
        qp.drawRect(QRect(self.begin, self.end))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            print('Quit')
            QApplication.restoreOverrideCursor();
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
        QApplication.processEvents()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.is_snipping = False
        self.repaint()
        QApplication.processEvents()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        self.snipped_image = img
        QApplication.restoreOverrideCursor()
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
            words_pos = english_meaning = chinese_meaning = example = ''
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
