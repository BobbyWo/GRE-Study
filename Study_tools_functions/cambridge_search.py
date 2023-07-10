from selenium import webdriver
from selenium.webdriver.common.by import By


class cambridge_search():
    def __init__(self):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome("selenium_driver/chromedriver.exe")
        self.driver = driver
        self.url = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/"
        self.driver.get(self.url)

    def search(self, search_word):
        search_box = self.driver.find_element(By.XPATH, "//*[@id='searchword']")
        search_box.clear()
        search_box.send_keys(search_word)
        search_button = self.driver.find_element(By.CLASS_NAME, "bo.iwc.iwc-40.hao.lb0.cdo-search-button.lp-0")
        search_button.click()
        word_dict_search = ""
        words = self.driver.find_elements(By.CLASS_NAME, "headword.hdb.tw-bw.dhw.dpos-h_hw")
        pos = self.driver.find_elements(By.CLASS_NAME, "pos.dpos")
        definitions = self.driver.find_elements(By.CLASS_NAME, "sense-body.dsense_b")
        list_defin = []
        defin_dict = dict()
        for index in range(len(words)):
            same_pos_different_meanings = definitions[index].find_elements(By.CLASS_NAME, "def-block.ddef_block")
            for mean in same_pos_different_meanings:
                word_dict_search += words[index].text + "\n"
                word_dict_search += "({0})".format(pos[index].text) + "\n"
                english_meaning = mean.find_element(By.CLASS_NAME, "def.ddef_d.db").text
                chinese_meaning = mean.find_element(By.CLASS_NAME, "trans.dtrans.dtrans-se.break-cj").text
                example = mean.find_elements(By.CLASS_NAME, "examp.dexamp")
                example = example[0].text if len(example) != 0 else "no example found"
                word_dict_search += "english_meaning:\n" + english_meaning + "\n"
                word_dict_search += "chinese_meaning:\n" + chinese_meaning + "\n"
                word_dict_search += "example:\n" + example + "\n"
                defin_dict["words"] = words[index].text
                defin_dict["pos"] = pos[index].text
                defin_dict["english_meaning"] = english_meaning
                defin_dict["chinese_meaning"] = chinese_meaning
                defin_dict["example"] = example
                list_defin.append(defin_dict)
                defin_dict = {}
                word_dict_search = ""
        return list_defin