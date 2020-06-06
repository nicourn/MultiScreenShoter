import configparser
import os
import socket
from tools.hotkeyer import KeyListener
from tools.screenshoter import ScreenShoter, ScreenFromTime

config = configparser.ConfigParser()
config.read("config.ini")

pause = int(config["Setting"]["pause"])
host = config["Setting"]["host"]
port = int(config["Setting"]["port"])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print("Connected")

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
    img_b: bytes = img[0].tobytes()
    size = 1024
    i = 0
    while size * i <= len(img_b):
        to_send = img_b[size * i : size*(i + 1)]
        s.send(to_send)
        i += 1



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