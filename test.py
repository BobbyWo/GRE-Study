import os
from pprint import pprint

from Study_tools_functions import File_io
#
# word_list = []
# file_io = File_io.file_io()
# path = "C:\\Users\\two\\Documents\\GRE-Study\\vocab_source\\GRE_kaplan_book"
# path_2 = "C:\\Users\\two\\Documents\\GRE-Study\\vocab_source\\GRE_kaplan_book_24-25"
# print(a)

# full_chapter_vocab = []
# full_chapter_meaning = []
# full_chapter_example = []
#
# for x in os.listdir(path_2):
#     section_path = os.path.join(path_2,x)
#     for y in os.listdir(section_path):
#         file = os.path.join(section_path,y)
#         if(y.__contains__("vocab")):
#             vocab_list = file_io.readVocabFile(file)
#             full_chapter_vocab.extend(vocab_list)
#         elif(y.__contains__("meaning")):
#             meaning_list = file_io.readMeaningfile(file)
#             full_chapter_meaning.extend(meaning_list)
#         else:
#             example_list = file_io.readExampleFile(file)
#             full_chapter_example.extend(example_list)

# print(full_chapter_example)
# for x in full_chapter_vocab:
#     print(x.split("\t")[0])
# print(full_chapter_meaning)
# print(full_chapter_example)

# copy_path = "C:\\Users\\two\\Documents\\GRE-Study\\vocab_source\\full_chapter\\GRE_kaplan_book_24-25"
# for x in (full_chapter_example):
#     file_io.writeVocabFile(copy_path,"example.txt",x)



a = '''devalued
tarnished
ridiculed
vituperated
impaired
vast
meager
unique
color
hardiness
delicacy
ignoring
lacking
needing
anecdotal
imagined
nominal
undertake
eschew
supplement
quotidian
latent
arresting
disingenuous
lax
authoritarian
hinted at
suggested
manifest
dilapidation
depilation
radiance
arid
calm
humid
waiting
unprepared
anxious
inundated
soaked
sprayed
selected
established
appropriated
bestowed
suggested
proposed
After
Although
Inasmuch as
Considering
While
Because
overwhelm
diminish
obviate
mitigate
eliminate
belittle
indignantly
mournfully
spitefully
bitterly
soberly
melancholically'''


b = a.split("\n")
c = [b[i:i+20] for i in range(0,len(b),20)]

print(c)