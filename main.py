import configparser
import os
from tools.hotkeyer import KeyListener
from tools.screenshoter import ScreenShoter, ScreenFromTime

config = configparser.ConfigParser()
config.read("config.ini")
pause = int(config["Setting"]["pause"])

shoter = ScreenShoter()
from_time = ScreenFromTime(shoter, pause)
from_key = KeyListener(shoter)
to_remove = []

area_num = int(config["Setting"]["area_num"])
for i in range(area_num):
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
    print("Sended")



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
