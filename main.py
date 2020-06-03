from screenshoter import ScreenShoter, ScreenFromTime
from hotkeyer import KeyListener
import os, time

from_time = ScreenFromTime(ScreenShoter("time", "main/"), 3)
from_key = KeyListener(ScreenShoter("key", "key/"))
for i in range(3):
    from_key.screen_shoter.add_area()
    img = ScreenShoter.queue.get()
    img[0].save(img[1])
    from_key.screen_shoter.fix_coord()
    to_remove = img
    os.remove(img[1])

from_key.start()
from_time.start()



def send(img):
    print("Sending...")
    time.sleep(0.1)
    print("Sended")

try:
    while True:
        img = ScreenShoter.queue.get()

        ishotkey = img[1].startswith("key")
        for cached_img in range(100):
            notequal = img[0].tobytes() != to_remove[0].tobytes()

        if ishotkey or notequal:
            send(img)
        else:
            print("Not send")

        to_remove = img

except:
    dirs = os.listdir()
    for dir in dirs:
        if os.path.isdir(dir) and dir[0].isalpha():
            os.removedirs(dir)


