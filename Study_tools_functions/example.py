import os

from Study_tools_functions import File_io,cambridge_search

cambridge = cambridge_search.cambridge_search()
path_prefix = 'C:/Users/two/Documents/GRE-Study'
file_io = File_io.file_io()
TPO_book_file_path = path_prefix + "/vocab_source/TPO_Book"
chapter_list = os.listdir(TPO_book_file_path)
defin_list = []
content = file_io.readVocabFile(TPO_book_file_path)
for i,chapter in enumerate(chapter_list):
    if(i == 0):
        chapter_path = TPO_book_file_path + "/" + chapter
        vocab_path = chapter_path + "/" + "vocab.txt"
        meaning_path = chapter_path + "/" + "meaning.txt"
        vocabs = file_io.readVocabFile(vocab_path)
        meanings = file_io.readMeaningfile(meaning_path)
        for i,word in enumerate(vocabs):
            # print(word.split("\t")[0])
            # print(meanings[i].split("\n")[1])
            meaning = meanings[i].split("\n")[1]
            same_meaning = False
            defin_list = cambridge.Enhance_search(word.split("\t")[0])
            for defin in defin_list:
                if dict(defin).get("english_meaning") == meaning:
                    print("choose this la :" + meaning)
                    same_meaning = True
            # if not same_meaning:
            #     print("cannot find this meaning")