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
            if(words.__contains__('')):
                words.remove('')
            vocab_list.extend(words)
        return vocab_list

    def readMeaningfile(self,file_path):
        vocab_list = []
        with open(file_path,encoding="utf-8") as f:
            lines = f.read()
            lines = lines.replace("\xa0"," ")
            words = lines.split("\n")
            for word in words:
                if(word == ''):
                    continue
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

    def writeVocabFile(self,file_path,file_name,content):
        content = str(content).replace("\n","\t")
        file_path = os.path.join(file_path,file_name)
        file_exists = os.path.exists(file_path)
        if(not file_exists):
            with open(file_path,'w', encoding="utf-8") as f:
                f.writelines(content + "\n")
                f.close()
        else:
            with open(file_path, 'a', encoding="utf-8") as f:
                f.writelines(content + "\n")
                f.close()

    def writeMeaningFile(self,file_path,file_name,content):
        content = str(content).replace("\n\n","")
        file_path = os.path.join(file_path, file_name)
        file_exists = os.path.exists(file_path)
        if(not file_exists):
            with open(file_path,'w', encoding="utf-8") as f:
                f.write(content + "\n")
                f.close()
        else:
            with open(file_path, 'a', encoding="utf-8") as f:
                f.writelines(content+ "\n")
                f.close()

    def writeExampleFile(self,file_path,file_name,content):
        # content = str(content).replace("\n\n","")
        file_path = os.path.join(file_path, file_name)
        file_exists = os.path.exists(file_path)
        if(not file_exists):
            with open(file_path,'w', encoding="utf-8") as f:
                f.write(content + "\n")
                f.close()
        else:
            with open(file_path, 'a', encoding="utf-8") as f:
                f.writelines(content+ "\n")
                f.close()

    def write_file(self,file_path,file_name,content):
        file_path = os.path.join(file_path, file_name)
        file_exists = os.path.exists(file_path)
        if (not file_exists):
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(content + "\n")
                f.close()
        else:
            with open(file_path, 'a', encoding="utf-8") as f:
                f.writelines(content + "\n")
                f.close()