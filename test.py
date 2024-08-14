import os
from pprint import pprint

from Study_tools_functions import File_io

word_list = []
file_io = File_io.file_io()
path = "C:\\Users\\two\\Documents\\GRE-Study\\vocab_source\\GRE_kaplan_book"
path_2 = "C:\\Users\\two\\Documents\\GRE-Study\\vocab_source\\barron_800"

full_chapter_vocab = []
full_chapter_meaning = []
full_chapter_example = []
#
for x in os.listdir(path_2):
    section_path = os.path.join(path_2,x)
    for y in os.listdir(section_path):
        file = os.path.join(section_path,y)
        if(y.__contains__("vocab")):
            vocab_list = file_io.readVocabFile(file)
            full_chapter_vocab.extend(vocab_list)
        elif(y.__contains__("meaning")):
            meaning_list = file_io.readVocabFile(file)
            full_chapter_meaning.extend(meaning_list)
        else:
            example_list = file_io.readExampleFile(file)
            full_chapter_example.extend(example_list)




copy_path = "C:\\Users\\two\\Documents\\GRE-Study\\vocab_source\\full_chapter\\barron_800"
for x in (full_chapter_meaning):
    file_io.writeVocabFile(copy_path,"meaning.txt",x)
