import random
import os

def pick(list):
    new_list = []
    if(len(list) >= 5):
        vocab_list = random.sample(list,5)
        new_list.extend(vocab_list)
    else:
        vocab_list = random.sample(list, len(list))
        new_list.extend(vocab_list)
    for word in new_list:
        print(word)
    return new_list
def enter_choice():

    val = input("Enter your Choice(Y/N): ")
    if val == "y" or val == "Y":
        return True

def readfile():
    dir = os.listdir("GRE_kaplan_book/studied/")
    vocab_list = []
    for file in dir:
        if(file.__contains__("txt")):
            with open(os.path.join("GRE_kaplan_book/studied/", file)) as f:
                lines = f.read()
                words = lines.split("\n")
                vocab_list.extend(words)
    while len(vocab_list) > 0:
        random_vocab_list = pick(vocab_list)
        if enter_choice():
            for word in random_vocab_list:
                vocab_list.remove(word)


readfile()