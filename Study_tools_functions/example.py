import os

from Study_tools_functions import cambridge_search,File_io

file_io = File_io.file_io()
cambridge = cambridge_search.cambridge_search()
folder_path = "C:/Users/User/Documents/image_to_string/vocab_source"
TPO_path = "TPO_Book"

current_path = os.path.join(folder_path,TPO_path)
for i,chapter in enumerate(os.listdir(current_path)):
    chapter_path = os.path.join(current_path,chapter)
    vocabs = file_io.readVocabFile(os.path.join(chapter_path,"vocab.txt"))
    meanings = file_io.readVocabFile(os.path.join(chapter_path, "meaning.txt"))
    for i,word in enumerate(vocabs):
        same_meaning = False
        curr_word = word.split("\t")[0]
        curr_meaning = meanings[i].split("\t")[0]
        defin_list = cambridge.Enhance_search(curr_word)
        for defin in defin_list:
            selected_meaning = dict(defin).get("english_meaning")
            if(selected_meaning == curr_meaning):
                example = dict(defin).get("example")
                example = example.replace("\n", "\t")
                print(example)
                same_meaning = True
                file_io.writeExampleFile(chapter_path, "example.txt", example)