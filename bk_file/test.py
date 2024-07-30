import json
import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import qdarkstyle
import pyperclip

from PyQt5.QtCore import Qt
from Study_tools_functions import notion, cambridge_search, File_io
from Study_tools_functions.Snip_window import SnipWidget
from UI_File.window.matching_game_window import MatchingGameWindow
from UI_File.button.UI_button import UI_button
class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.win_width = 900
        self.win_height = 1000
        self.horizontal_margin = 20
        self.vertical_margin = 10
        self.current_chapter = ""
        self.file_io = File_io.file_io()
        self.kaplan_file_path = "vocab_source/GRE_kaplan_book"
        self.Kaptest_file_path = "vocab_source/Kaptest_Vocab"
        self.Quizlet_file_path = "vocab_source/Quizlet_Vocab"
        self.TOFEL_book_file_path = "vocab_source/TOFEL_book_Vocab"
        self.TOFEL_online_file_path = "vocab_source/TOEFL_Vocab"
        self.TPO_book_file_path = "vocab_source/TPO_Book"
        self.kaplan_vocab_table_id = "0bc17826-0f8a-4497-bcf5-9923a205b314"
        self.new_tofel_vocab_120_table_id = "70a74c01-2fc3-4eec-9420-4f08a37f2f3a"
        f = open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "config.json"))
        self.data = json.load(f)
        self.Notion_call_enabled = self.data["Notion_call_enabled"] == 'Y'
        # self.setGeometry(50, 50, self.win_width, self.win_height)
        self.setWindowTitle("GRE study tools")
        self.dict_search = cambridge_search.cambridge_search()
        if self.Notion_call_enabled:
            self.notion_call = notion.notion_API()
        self.initUI()

    def sourceOnChanged(self,text):
        self.current_chapter = text
        print(self.current_chapter)
    def initUI(self):
    #     self.initializedNoti()


        GRE_layout = self.init_GRE_layout()
        insert_chapter_layout = self.init_insert_chapter_layout()
        search_word_layout = self.init_search_word_layout()
        search_button_layout = self.init_search_button_layout()
        noti_box_layout = self.init_noti_box_layout()

        ## final UI layout
        container = QWidget()
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addLayout(GRE_layout)
        layout.addStretch(1)
        layout.addLayout(insert_chapter_layout)
        layout.addStretch(1)
        layout.addLayout(search_word_layout)
        layout.addStretch(1)
        layout.addLayout(search_button_layout)
        layout.addStretch(1)
        layout.addLayout(noti_box_layout)
        layout.addStretch(1)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def init_GRE_layout(self):
        GRE_layout = QHBoxLayout()
        GRE_layout.setAlignment(Qt.AlignLeft)
        GRE_layout.setContentsMargins(self.horizontal_margin, self.vertical_margin, self.horizontal_margin, 0)
        GRE_layout.setSpacing(50)

        I_T_S_Question = UI_button("Image to String(Question)")
        I_T_S_Question.clicked.connect(self.Question_Button_clicked)
        GRE_layout.addWidget(I_T_S_Question)

        I_T_S_Answer = UI_button("Image to String(Answer)")
        I_T_S_Answer.clicked.connect(self.Answer_Button_clicked)
        GRE_layout.addWidget(I_T_S_Answer)

        createTable = UI_button("Create Table")
        createTable.clicked.connect(self.CreateTable_Button_clicked)
        GRE_layout.addWidget(createTable)

        paraTrans = UI_button("Image to String(translation)")
        paraTrans.clicked.connect(self.ParagraphTranslation_Button_clicked)
        GRE_layout.addWidget(paraTrans)
        return GRE_layout

    def init_insert_chapter_layout(self):
        insert_chapter_layout = QHBoxLayout()
        insert_chapter_layout.setContentsMargins(self.horizontal_margin, self.vertical_margin, self.horizontal_margin, 0)

        combo = QComboBox()
        combo.addItem("-")
        f = open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "config.json"))
        data = json.load(f)
        sourceDir = data["vocab_source_path"]
        for source in os.listdir(sourceDir):
            combo.addItem(source)
        combo.activated[str].connect(self.sourceOnChanged)
        insert_chapter_layout.addWidget(combo)
        return insert_chapter_layout

    def init_search_word_layout(self):
        search_word_layout = QVBoxLayout()
        search_word_layout.setContentsMargins(self.horizontal_margin, self.vertical_margin, self.horizontal_margin, 0)
        searchDirlabel = QLabel()
        searchDirlabel.setText('search Word')
        searchDirlabel.adjustSize()
        search_word_layout.addWidget(searchDirlabel)


        self.searchWord = QLineEdit()
        self.searchWord.setFixedSize(self.win_width - 20, 20)
        search_word_layout.addWidget(self.searchWord)
        return search_word_layout
    
    def init_search_button_layout(self):
        search_button_layout = QHBoxLayout()
        search_button_layout.setAlignment(Qt.AlignLeft)
        search_button_layout.setContentsMargins(self.horizontal_margin, self.vertical_margin, self.horizontal_margin, 0)
        search_button_layout.setSpacing(50)

        vocab_search_button = UI_button("Question Vocab Search")
        vocab_search_button.clicked.connect(self.Question_Vocab_Search_Button_clicked)
        search_button_layout.addWidget(vocab_search_button)

        search_and_insert_button = UI_button("Search and insert into table")
        search_and_insert_button.clicked.connect(self.insertIntoTable)
        search_button_layout.addWidget(search_and_insert_button)

        play_game_button = UI_button("Play matching game")
        play_game_button.clicked.connect(self.Matching_Button_Clicked)
        search_button_layout.addWidget(play_game_button)
        return search_button_layout
    
    def init_noti_box_layout(self):
        noti_box_layout = QVBoxLayout()
        noti_box_layout.setContentsMargins(self.horizontal_margin, self.vertical_margin, self.horizontal_margin, 0)
        self.notificationBox = QGroupBox("Notification Box")
        self.notificationBox.setFixedSize(self.win_width - 20, 500)
        self.layout = QHBoxLayout()
        self.notificationText = QLabel()
        self.layout.addWidget(self.notificationText)
        self.notificationBox.setLayout(self.layout)
        noti_box_layout.addWidget(self.notificationBox)
        return noti_box_layout

    def initializedNoti(self):
        self.notificationBox.setFixedSize(self.win_width - 20, 500)
        self.layout = QHBoxLayout()
        self.notificationText = QLabel(self)
        self.layout.addWidget(self.notificationText)
        self.notificationBox.setLayout(self.layout)
    #
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
        if self.Notion_call_enabled:
            self.notion_call.create_table()

    def ParagraphTranslation_Button_clicked(self):
        self.snipWin = SnipWidget("paraTrans", self)
        self.snipWin.notification_signal.connect(self.reset_notif_text)
        self.snipWin.show()
        self.notificationText.setText("paragraph translation button clicked")
        self.update_notif()
    #
    def Matching_Button_Clicked(self):
        self.matching_game = MatchingGameWindow()
        self.matching_game.show()
    def insertIntoTable(self):
        self.Question_Vocab_Search_Button_clicked(insert=True)
        if(len(self.content_list) == 0 ):
            return
        if(not self.hasChoice):
            if self.Notion_call_enabled:
                self.notion_call.insert_table_row(self.content)
            self.file_io.writeVocabFile(os.path.join(self.TOFEL_book_file_path, "test"),"vocab.txt",self.content[0])
            self.file_io.writeMeaningFile(os.path.join(self.TOFEL_book_file_path, "test"),"meaning.txt",self.content[1] + "\t" + self.content[2])

    def Question_Vocab_Search_Button_clicked(self,insert=False):
        search_word = self.searchWord.text()
        # definition = self.dict_search.search(search_word)
        definition = self.dict_search.Enhance_search(search_word)
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
            self.giveChoice(defiList,insert)
        else:
            self.hasChoice = False
            if self.notificationText:
                self.notificationBox.setFixedSize(self.win_width - 20, 500)
            else:
                self.notificationText = QLabel(self)
            self.notificationText.setText(output_str)
            if self.layout == None:
                self.layout = QHBoxLayout()
            self.notificationBox.setLayout(self.layout)
            pyperclip.copy(output_str)
        # self.reset_notif_text()

    def giveChoice(self, defiList,insert):
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
            self.choice_dict[key].clicked.connect(lambda checked, a=key,b=insert: self.choiceButtonClicked(a,b))

            choice.addWidget(value)
            self.layout.addLayout(choice)
        if self.layout == None:
            self.layout = QHBoxLayout()
        self.notificationBox.setLayout(self.layout)
        self.notificationBox.setFixedSize(self.win_width - 20, 500)
    #
    def choiceButtonClicked(self, key,insert):
        pyperclip.copy(self.choice_dict[key].property("defi"))
        self.content = (self.choice_dict[key].property("content"))
        if self.Notion_call_enabled:
            self.notion_call.insert_table_row(self.content)
        if(insert):
            self.file_io.writeVocabFile(os.path.join(self.TOFEL_book_file_path, "test"), "vocab.txt", self.content[0])
            self.file_io.writeMeaningFile(os.path.join(self.TOFEL_book_file_path, "test"), "meaning.txt",
                                          self.content[1] + "\t" + self.content[2])
        for all in self.notificationBox.children():
            all.deleteLater()
        self.initializedNoti()

    def onChanged(self, text):
        temp_text = f'Page changed to {text}. \n'
        self.notificationText.setText(temp_text)
        if self.Notion_call_enabled:
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
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MyWindow()
    win.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    window()