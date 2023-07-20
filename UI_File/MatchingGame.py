import os
import random
from pprint import pprint

from UI_File.movable_widget import MyMovableWidget
from Study_tools_functions import notion
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import math
from Study_tools_functions import File_io

class MatchingGameWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.notion_call = notion.notion_API()
        self.setFixedSize(900, 550)
        self.setContentsMargins(25, 5, 25, 5)
        self.vocab_dict = {}
        self.pages_stackWidget = QStackedWidget()
        self.file_io = File_io.file_io()
        self.confirmButtonSet = False
        self.init_pages()

        container = QWidget()
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addLayout(self.select_chapter)
        layout.addStretch(1)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def init_pages(self):
        # combo box to select chapter
        self.select_chapter = QHBoxLayout()
        self.combo = QComboBox()
        self.combo.addItem("-")
        self.sourceDir = "C:\\Users\\02003964\\PycharmProjects\\image_to_string\\vocab_source"
        for source in os.listdir(self.sourceDir):
            self.combo.addItem(source)
        self.combo.activated[str].connect(self.sourceOnChanged)
        self.select_chapter.addWidget(self.combo)

    def setConfirmButton(self):
        confirm_button = QPushButton()
        confirm_button.setText("confirm")
        confirm_button.clicked.connect(self.confirmButtonClicked)
        self.select_chapter.addWidget(confirm_button)

    def confirmButtonClicked(self):
        for vocab_file in os.listdir(self.vocab_files):
            # get vocab word
            if (vocab_file.__contains__("vocab")):
                word_file_path = os.path.join(self.vocab_files, vocab_file)
            # get vocab meaning
            if (vocab_file.__contains__("meaning")):
                meaning_file_path = os.path.join(self.vocab_files, vocab_file)
        if (word_file_path):
            word_list = self.file_io.readVocabFile(word_file_path)
        if (meaning_file_path):
            meaning_list = self.file_io.readMeaningfile(meaning_file_path)
        for index, word in enumerate(word_list):
            self.vocab_dict[word] = meaning_list[index]

        print(len(word_list))
        shuffled_words = random.sample(word_list, len(word_list))
        page_index = 0
        self.Chapter_answer_list = []
        self.Chapter_user_answer_list = [-1] * len(word_list)
        self.Chapter_answer_box_list = []
        while(len(shuffled_words)>0):
            if(len(shuffled_words) >= 5):
                random_words = shuffled_words[0:5]
            else:
                random_words = shuffled_words[0:len(shuffled_words)]
            index_list = []
            for word in random_words:
                index_list.append(word_list.index(word))
                shuffled_words.remove(word)
            page_container = self.setup_vocab(random_words,meaning_list,index_list,page_index)
            self.pages_stackWidget.addWidget(page_container)
            page_index += 1
            self.Chapter_answer_list.extend(index_list)
        self.setCentralWidget(self.pages_stackWidget)
    def sourceOnChanged(self, text):
        if (text == "-"):
            return
        chapter_box = QComboBox()
        self.book_chapter_dir = os.path.join(self.sourceDir, text)
        chapter_box.addItem("-")
        # chapter_box.addItem("All")
        for chapter in os.listdir(self.book_chapter_dir):
            chapter_box.addItem(chapter)
        self.select_chapter.addWidget(chapter_box)
        chapter_box.activated[str].connect(self.chapterOnChanged)

    def chapterOnChanged(self, chapter):
        if (chapter == "-"):
            return
        # if(chapter == "All"):
        #     self.vocab_files
        self.vocab_files = os.path.join(self.book_chapter_dir, chapter)
        if(not self.confirmButtonSet):
            self.setConfirmButton()
            self.confirmButtonSet = True

    def setup_vocab(self,words_list,meaning_list,index_list,page_index):
        one_page_layout = QVBoxLayout()

        #set up word
        word_layout = self.setup_word(words_list)
        one_page_layout.addStretch(1)
        one_page_layout.addLayout(word_layout)
        #set up answer
        answer_layout = self.setup_answer(meaning_list,index_list)
        one_page_layout.addStretch(1)
        one_page_layout.addLayout(answer_layout)
        #set up button
        button_layout = self.setup_button(page_index)
        one_page_layout.addStretch(1)
        one_page_layout.addLayout(button_layout)

        one_page_layout.addStretch(1)
        self.takeCentralWidget()
        new_container = QWidget()
        new_container.setLayout(one_page_layout)
        return new_container

    def setup_word(self,words_list):
        #set up word
        words_layout = QHBoxLayout()
        word_widget_list = []
        self.page_answerbox_list = []
        for index,word in enumerate(words_list):
            word_widget = QLabel(word)
            word_widget.setStyleSheet("border: 1px solid black;border-radius: 10px ")
            word_widget.setContentsMargins(15, 5, 15, 5)
            word_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            word_widget_list.append(word_widget)
            answer_box = QLabel()
            answer_box.setFixedSize(161,200)
            answer_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            answer_box.setStyleSheet("border: 1px solid black;")
            self.page_answerbox_list.append(answer_box)
        self.Chapter_answer_box_list.append(self.page_answerbox_list)
        for index,temp_word in enumerate(word_widget_list):
            word_answer_layout = QVBoxLayout()
            word_answer_layout.addStretch(1)
            word_answer_layout.addWidget(temp_word)
            word_answer_layout.addStretch(1)
            word_answer_layout.addWidget(self.page_answerbox_list[index])
            words_layout.addLayout(word_answer_layout)
        return words_layout

    def setup_answer(self,meaning_list,index_list):
        # set up answer
        answer_layout = QHBoxLayout()
        self.answer_list = []
        for index, word_index in enumerate(index_list):
            item = MyMovableWidget(meaning_list[word_index])
            item.posChanged.connect(self.checkCoverage)
            item.setWordWrap(True)
            item.setStyleSheet("border: 1px solid black;padding-top: 10px;padding-left: 10px;padding-right: 10px")
            item.setFixedSize(161, 200)
            item.set_data(word_index)
            self.answer_list.append(item)
        random.shuffle(self.answer_list)
        for answer in self.answer_list:
            answer_layout.addWidget(answer)
        return answer_layout

    def setup_button(self,page_index):
        #set Button
        button_layout = QHBoxLayout()
        if page_index != 0:
            back_button = QPushButton("Back")
            back_button.clicked.connect(lambda checked, page_index=page_index: self.backButtonClicked(page_index))
            button_layout.addWidget(back_button)

        next_button = QPushButton("Next")
        next_button.clicked.connect(lambda checked,page_index=page_index:self.nextButtonClicked(page_index))
        button_layout.addWidget(next_button)
        # print(self.vocab_dict.__len__()/5)
        # print(round(self.vocab_dict.__len__()/5))
        # print(page_index)
        # if(isinstance(self.vocab_dict.__len__()/5, int)):
        print(self.vocab_dict.__len__())
        page_index+= 1
        if( page_index == math.ceil(self.vocab_dict.__len__()/5)):
            submit_button = QPushButton("Submit")
            submit_button.clicked.connect(self.submitButtonClicked)
            button_layout.addWidget(submit_button)

        return button_layout

    def checkCoverage(self, box_list):
        Current_page_answerbox_list = (self.Chapter_answer_box_list[self.pages_stackWidget.currentIndex()])
        embedded = False
        for index,box in enumerate(Current_page_answerbox_list):
                overlap_height = box.height()- abs(box.geometry().topLeft().y()-box_list[0].y())
                overlap_width = box.width()- abs(box.geometry().topLeft().x()-box_list[0].x())
                if overlap_height < 0 or overlap_width<0:
                    continue
                overlap_area = overlap_width*overlap_height
                box_area = box.width()*box.height()
                coverage_percentage = overlap_area / box_area
                if coverage_percentage > 0.5:
                    embedded = True
                    box_list[1].embbed_to_answer_box(index)
                    self.attach_to_answer_box(box,index,box_list[1])
                    break
        if(not embedded):
            if box_list[1].get_embbed_answer_box() != -1:
                self.Chapter_user_answer_list[self.pages_stackWidget.currentIndex() * 5 + box_list[1].get_embbed_answer_box()] = -1
                box_list[1].remove_from_answer_box()
            box_list[1].return_original_pos()


    def attach_to_answer_box(self,answer_box,answer_box_index,answer):
        answer.move(answer_box.pos())
        self.Chapter_user_answer_list[self.pages_stackWidget.currentIndex() * 5 + answer_box_index] = answer.get_data()
    def backButtonClicked(self,page_index):
        self.pages_stackWidget.setCurrentIndex(page_index - 1)
    def nextButtonClicked(self, page_index):
        self.pages_stackWidget.setCurrentIndex(page_index + 1)
        print(page_index + 1)
    def submitButtonClicked(self):
        marks = 0
        for index,answer in enumerate(self.Chapter_answer_list):
            if(answer == self.Chapter_user_answer_list[index]):
                marks += 1
        result_marks = (marks/len(self.Chapter_user_answer_list))*100
        self.file_io.write_file(self.vocab_files,"marks.txt",str(result_marks))
        print(self.Chapter_answer_list)
        print(self.Chapter_user_answer_list)
        self.deleteLater()

# app = QApplication([])
# w = MainWindow()
# w.show()
#
# app.exec_()
