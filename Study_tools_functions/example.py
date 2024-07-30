import os

from Study_tools_functions import cambridge_search,File_io

file_io = File_io.file_io()
# cambridge = cambridge_search.cambridge_search()
folder_path = "../vocab_source"
TPO_path = "TOFEL_book_Vocab"
TPO_book = "TPO_Book"

current_path = os.path.join(folder_path,TPO_book)
# for i,chapter in enumerate(os.listdir(current_path)):
#     if(chapter == 'word_list_29' or chapter == 'word_list_30'):
#
#         print(chapter)
#         chapter_path = os.path.join(current_path,chapter)
#         vocabs = file_io.readVocabFile(os.path.join(chapter_path,"vocab.txt"))
#         meanings = file_io.readVocabFile(os.path.join(chapter_path, "meaning.txt"))
#         for index,word in enumerate(vocabs):
#             same_meaning = False
#             curr_word = word.split("\t")[0]
#             curr_meaning = meanings[index].split("\t")[0]
#             defin_list = cambridge.Enhance_search(curr_word)
#             for defin in defin_list:
#                 selected_meaning = dict(defin).get("english_meaning")
#                 if(selected_meaning == curr_meaning):
#                     example = dict(defin).get("example")
#                     example = example.replace("\n", "\t")
#                     print(example)
#                     same_meaning = True
#                     file_io.writeExampleFile(chapter_path, "example.txt", example)
#             if not same_meaning:
#                 print(chapter," : ",curr_word)



for i,chapter in enumerate(os.listdir(current_path)):
    chapter_path = os.path.join(current_path, chapter)
    vocabs = file_io.readVocabFile(os.path.join(chapter_path,"vocab.txt"))
    meanings = file_io.readVocabFile(os.path.join(chapter_path, "meaning.txt"))
    examples = file_io.readVocabFile(os.path.join(chapter_path, "example.txt"))
    print(chapter,[len(vocabs),len(meanings),len(examples),len(vocabs)==len(meanings) and len(vocabs) == len(examples)])