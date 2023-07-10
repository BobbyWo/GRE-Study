import os


class file_io():
    def __init__(self, dir_path=None):
        self.dir_path = dir_path
    def readWholeDir(self):
        dir = os.listdir(self.dir_path)
        vocab_list = []
        for file in dir:
            if (file.__contains__("txt")):
                with open(os.path.join(self.dir_path, file)) as f:
                    lines = f.read()
                    words = lines.split("\n")
                    vocab_list.extend(words)

    def readVocabFile(self,file_path):
        vocab_list = []
        with open(file_path,encoding='utf-8') as f:
            lines = f.read()
            words = lines.split("\n")
            vocab_list.extend(words)
        return vocab_list

    def readMeaningfile(self,file_path):
        vocab_list = []
        with open(file_path,encoding="utf-8") as f:
            lines = f.read()
            lines = lines.replace("\xa0"," ")
            words = lines.split("\n")
            for word in words:
                word = word.split("\t")
                english_meaning = "Null"
                chinese_meaning = "Null"
                if(word[0]):
                    english_meaning = word[0].strip()
                if (len(word) > 1):
                    chinese_meaning = word[1].strip()
                defin = ""
                if(english_meaning):
                    defin += "english_meaning:\n" + english_meaning + "\n"
                if(chinese_meaning):
                    defin += "chinese_meaning:\n" + chinese_meaning
                vocab_list.append(defin)
        return  vocab_list