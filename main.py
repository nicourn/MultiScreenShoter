from tools.screenshoter import ScreenShoter, ScreenFromTime
from tools.hotkeyer import KeyListener
import os, time

os.mkdir("cache")

from_time = ScreenFromTime(ScreenShoter("time", "cache/main/"), 3)
from_key = KeyListener(ScreenShoter("key", "cache/key/"))
to_remove = []
for i in range(3):
    from_key.screen_shoter.add_area()
    img = ScreenShoter.queue.get()
    img[0].save(img[1])
    from_key.screen_shoter.fix_coord()
    os.remove(img[1])

from_key.start()
# from_time.start()



def send(img):
    print(f"{img[1]} sending...")
    img[0].save(img[1])
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

except :
    print("err")
    os.chdir("cache")
    dirs = os.listdir()
    for dir in dirs:
        if os.path.isdir(dir) and dir[0].isalpha():
            os.removedirs(dir)
    os.chdir("../")
    os.removedirs("cache")


