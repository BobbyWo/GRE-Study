import io
from pprint import pprint

with io.open('../vocab.txt', 'r', encoding='utf8') as f:
    words = f.readlines()
    for index,word in enumerate(words):
        if index%2 ==0:
            print(word.split('–')[0])
