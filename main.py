import os
import pytesseract
from PIL import Image
from pynput import keyboard, mouse
from pynput.mouse import Button, Controller
import pyscreenshot
import pyperclip
import json
import cambridge_search
import notion
from pprint import pprint

pressed_location_x = 0
pressed_location_y = 0
released_location_x = 0
released_location_y = 0


def i_t_s():
    file = os.listdir("./image")
    img_name = os.path.join("image", file[0])
    img = Image.open(img_name)
    s = str(pytesseract.image_to_string(img))
    s = s.replace('-\n', '')
    s = s.replace('\n', ' ')
    notion_call.paragraph_content(s, type="heading_3")
    # notion_call.create_table()
    # pyperclip.copy(s)
    # print(s)



def i_t_s_1():
    file = os.listdir("./image")
    img_name = os.path.join("image", file[0])
    img = Image.open(img_name)
    s = str(pytesseract.image_to_string(img))
    notion_call.paragraph_content(s, type="heading_3")
    # notion_call.create_table()
    # pyperclip.copy(s)
    # print(s)



def cap_image_to_string():
    global pressed_location_x
    global pressed_location_y
    global released_location_x
    global released_location_y
    if released_location_y <= pressed_location_y or released_location_x <= pressed_location_x:
        return
    print("a")
    pic = pyscreenshot.grab(bbox=(pressed_location_x, pressed_location_y, released_location_x, released_location_y))
    pic.save(os.path.join("./image", "test.png"))
    i_t_s()
    print("finished")


def cap_image_to_string_1():
    global pressed_location_x
    global pressed_location_y
    global released_location_x
    global released_location_y
    if released_location_y <= pressed_location_y or released_location_x <= pressed_location_x:
        return
    print("q")
    pic = pyscreenshot.grab(bbox=(pressed_location_x, pressed_location_y, released_location_x, released_location_y))
    pic.save(os.path.join("./image", "test.png"))
    i_t_s_1()
    print("finished")


def translation():
    global pressed_location_x
    global pressed_location_y
    global released_location_x
    global released_location_y
    if released_location_y <= pressed_location_y or released_location_x <= pressed_location_x:
        return
    print("t")
    pic = pyscreenshot.grab(bbox=(pressed_location_x, pressed_location_y, released_location_x, released_location_y))
    pic.save(os.path.join("./image", "test.png"))
    file = os.listdir("./image")
    img_name = os.path.join("image", file[0])
    img = Image.open(img_name)
    s = str(pytesseract.image_to_string(img))
    choice = s.split("\n")
    for word in choice:
        if (word == "" or len(word) == 0):
            continue
        definition = ""
        try:
            definition = dict_search.search(str(word).strip())
        except:
            content = [word, "", "", ""]
            notion_call.insert_table_row(content)
        # if len(definition) == 0:b   
        #     content = [word, "", "", ""]
        #     notion_call.insert_table_row(content)
        for defi in definition:
            words = dict(defi).get("words")
            pos = dict(defi).get("pos")
            words_pos = words + "\n" + f"({pos})"
            english_meaning = dict(defi).get("english_meaning")
            chinese_meaning = dict(defi).get("chinese_meaning")
            example = dict(defi).get("example")
            content = [words_pos, english_meaning, chinese_meaning, example]
            notion_call.insert_table_row(content)


def create_new_table():
    notion_call.create_table()


def paragraph_translation():
    print("p")
    s = str(pyperclip.paste())
    definition = dict_search.search(str(s).strip())
    pyperclip.copy(str(definition))


# mouse monitor
mouses = Controller()


def on_click(x, y, button, pressed):
    global pressed_location_x
    global pressed_location_y
    global released_location_x
    global released_location_y

    if button == Button.right:
        return False
    if (pressed):
        pressed_location_x, pressed_location_y = x, y
    elif (not pressed):
        released_location_x, released_location_y = x, y


if __name__ == '__main__':
    # def its():
    # os.remove(i_t_s())
    mouse_listener = mouse.Listener(
        on_click=on_click
    )
    key_listener = keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+a': cap_image_to_string,
        '<ctrl>+<alt>+t': translation,
        '<ctrl>+<alt>+n': create_new_table,
        '<ctrl>+<alt>+p': paragraph_translation,
        '<ctrl>+<alt>+q': cap_image_to_string_1})
    dict_search = cambridge_search.cambridge_search()
    notion_call = notion.notion_API()
    mouse_listener.start()
    key_listener.start()
    mouse_listener.join()
    key_listener.join()
