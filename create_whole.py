# import os
# from Study_tools_functions import File_io
#
# file_io = File_io.file_io()
# vocab_source = "./vocab_source"
# full_chapter_path  = os.path.join(vocab_source,"full_chapter")
# print(os.listdir(vocab_source))
# vocab_list = []
# meaning_list = []
# example_list = []
# for book in os.listdir(vocab_source):
#     if(book != "TPO_Book"):
#         continue
#     full_book_path = os.path.join(full_chapter_path,book)
#     if not os.path.exists(full_book_path):
#         os.mkdir(full_book_path)
#     curr_book_path = os.path.join(vocab_source,book)
#     # vocab_list = []
#     # meaning_list = []
#     # example_list = []
#     for x in os.listdir(curr_book_path):
#         path = os.path.join(curr_book_path,x)
#         for y in os.listdir(path):
#             z = os.path.join(path,y)
#             if(y.__contains__("vocab")):
#                 vocab = file_io.readVocabFile(z)
#                 vocab_list.extend(vocab)
#             elif(y.__contains__("meaning")):
#                 meaning = file_io.readVocabFile(z)
#                 meaning_list.extend(meaning)
#             else:
#                 example = file_io.readVocabFile(z)
#                 example_list.extend(example)
#
# for a in vocab_list:
#     file_io.writeVocabFile(full_book_path,"vocab.txt",a)
# for b in meaning_list:
#     file_io.writeVocabFile(full_book_path,"meaning.txt",b)
# for c in example_list:
#     file_io.writeVocabFile(full_book_path,"example.txt",c)
# # print(vocab_list)
# # print(meaning_list)
# # print(example_list)