import configparser
import os
import time

from tools.hotkeyer import KeyListener
from tools.screenshoter import ScreenShoter, ScreenFromTime

os.mkdir("cache")
config = configparser.ConfigParser()
config.read("config.ini")
pause = int(config["Setting"]["pause"])
from_time = ScreenFromTime(ScreenShoter("time", "cache/main/"), pause)
from_key = KeyListener(ScreenShoter("key", "cache/key/"))
to_remove = []

for i in range(int(config["Setting"]["area_num"])):
    from_key.screen_shoter.add_area()
    if i == 0:
        img = ScreenShoter.queue.get()
        img[0].save(img[1])
        to_remove.append(img)
    from_key.screen_shoter.fix_coord()
img = to_remove.pop()
os.remove(img[1])

from_key.start()
from_time.start()


def send(img):
    print(f"{img[1]} sending...")
    # img[0].save(img[1])
    time.sleep(0.1)
    print("Sended")


try:
    while True:
        img = ScreenShoter.queue.get()

        ishotkey = "key" in img[1]
        if ishotkey:
            send(img)
            continue

        notequal = True
        for i, cached_img in enumerate(to_remove):
            if img[2] == cached_img[2]:
                notequal = img[0].tobytes() != cached_img[0].tobytes()
                to_remove[i] = img
                break
        else:
            to_remove.append(img)

        if notequal:
            send(img)
        else:
            print("Not send")
except:
    os.chdir("cache")
    folders = os.listdir()
    for forlder in folders:
        if os.path.isdir(forlder) and forlder[0].isalpha() and forlder != "tools":
            os.removedirs(forlder)

    os.chdir("../")
    os.removedirs("cache")
