from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

import pyperclip

from Study_tools_functions import notion, cambridge_search
from Study_tools_functions.Snip_window import SnipWidget


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.win_width = 900
        self.win_height = 1000
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
        self.paraTrans.setText("Image to String(translation)")
        self.paraTrans.move(int((self.win_width / 4 * (x - 1)) + 10), 75)
        self.paraTrans.setFixedSize(150, 40)
        self.paraTrans.clicked.connect(self.ParagraphTranslation_Button_clicked)
        x += 1

        self.comment = QPushButton(self)
        self.comment.setText("Question Vocab Search")
        self.comment.move(10, 170)
        self.comment.setFixedSize(150, 40)
        self.comment.clicked.connect(self.Question_Vocab_Search_Button_clicked)

        # self.click_and_insert_table = QPushButton(self)
        # self.click_and_insert_table.setText("Search and insert into table")
        # self.click_and_insert_table.move(200, 170)
        # self.click_and_insert_table.setFixedSize(150, 40)
        # self.click_and_insert_table.clicked.connect(self.insertIntoTable)
        #
        # self.searchWordLable = QLabel(self)
        # self.searchWordLable.move(10, 125)
        # self.searchWordLable.setText('search Word')
        # self.searchWordLable.adjustSize()
        #
        # self.searchWord = QLineEdit(self)
        # self.searchWord.move(10, 145)
        # self.searchWord.setFixedSize(self.win_width - 20, 20)

        self.layout = QHBoxLayout()
        self.notificationBox = QGroupBox("Notification Box", self)
        self.notificationBox.move(10, 220)
        self.notificationText = QLabel(self)

        self.initializedNoti()

    def initializedNoti(self):
        self.notificationBox.setFixedSize(self.win_width - 20, 55)
        self.layout = QHBoxLayout()
        self.notificationText = QLabel(self)
        self.layout.addWidget(self.notificationText)
        self.notificationBox.setLayout(self.layout)

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

    def insertIntoTable(self):
        self.Question_Vocab_Search_Button_clicked()
        if(not self.hasChoice):
            self.notion_call.insert_table_row(self.content,"0bc17826-0f8a-4497-bcf5-9923a205b314")
    def Question_Vocab_Search_Button_clicked(self):
        search_word = self.searchWord.text()
        definition = self.dict_search.search(search_word)
        if len(definition) == 0:
            content = [search_word, "", "", ""]
        output_str = ''
        defiList = []
        self.content_list = []
        for defi in definition:
            words = dict(defi).get("words")
            pos = dict(defi).get("pos")
            words_pos = words + f"({pos})" + '\n\n'
            english_meaning = dict(defi).get("english_meaning") + '\n\n'
            chinese_meaning = dict(defi).get("chinese_meaning") + '\n\n'
            example = dict(defi).get("example") + '\n\n'
            output_str = words_pos + "english_meaning:\n" + english_meaning + "chinese_meaning:\n" + chinese_meaning + "example:\n" + example + '\n\n\n'
            defiList.append(output_str)
            self.content = [words +"\n" + f"({pos})",english_meaning,chinese_meaning,example]
            self.content_list.append(self.content)
        if len(defiList) > 1:
            self.hasChoice = True
            self.giveChoice(defiList)
        else:
            self.hasChoice = False
            if self.notificationText:
                self.notificationBox.setFixedSize(self.win_width - 20, 300)
            else:
                self.notificationText = QLabel(self)
            self.notificationText.setText(output_str)
            if self.layout == None:
                self.layout = QHBoxLayout()
            self.notificationBox.setLayout(self.layout)
            pyperclip.copy(output_str)
    def giveChoice(self, defiList):
        self.notificationText.deleteLater()
        self.choice_dict = {}
        for i, numDefi in enumerate(defiList):
            choice = QVBoxLayout()
            defi = QLabel(self)
            defi.setText(numDefi)
            defi.setWordWrap(True)
            defi.setFont(QFont('Arial', 11))
            defi.setStyleSheet("border: 1px solid black;padding-top:20px;padding-left:10px;padding-right:10px")
            choice.addWidget(defi)
            key = f"choiceButton{i}"
            value = QPushButton(self)
            value.setText("accept")
            value.setProperty("defi", defi.text())
            value.setProperty("content",self.content_list[i])
            self.choice_dict[key] = value
            self.choice_dict[key].clicked.connect(lambda checked, a=key: self.choiceButtonClicked(a))

            choice.addWidget(value)
            self.layout.addLayout(choice)
        if self.layout == None:
            self.layout = QHBoxLayout()
        self.notificationBox.setLayout(self.layout)
        self.notificationBox.setFixedSize(self.win_width - 20, 500)

    def choiceButtonClicked(self, key):
        pyperclip.copy(self.choice_dict[key].property("defi"))
        self.content = (self.choice_dict[key].property("content"))
        self.notion_call.insert_table_row(self.content, "0bc17826-0f8a-4497-bcf5-9923a205b314")
        for all in self.notificationBox.children():
            all.deleteLater()
        self.initializedNoti()

    def onChanged(self, text):
        temp_text = f'Page changed to {text}. \n'
        self.notificationText.setText(temp_text)
        self.notion_call.change_page(self.page[text])

    def reset_notif_text(self):
        self.notificationText.setText("Idle...")
        self.update_notif()

    def update_notif(self):
        self.notificationText.move(20, 155)
        self.notificationText.adjustSize()

    def define_notif_text(self, msg):
        print('notification was sent')
        self.notificationText.setText('notification was sent')
        self.update_notif()


def window():
    app = QApplication(sys.argv)

    win = MyWindow()
    win.show()

    sys.exit(app.exec_())


window()