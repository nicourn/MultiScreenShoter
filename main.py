from screenshoter import ScreenShoter, ScreenFromTime
from hotkeyer import KeyListener
import os

from_time = ScreenFromTime(ScreenShoter("time", "time/"), 3)
from_key = KeyListener(ScreenShoter("key", "key/"))

from_key.screen_shoter.get_area()
from_key.screen_shoter.fix_coord()

from_key.start()

from_time.start()
to_remove = []

try:
    while True:
        img = ScreenShoter.queue.get()
        # Пересылка изображения
        img[0].save(img[1])
        print(f"{img[1]} saved")

        if img[1].startswith("key") and len(to_remove) != 0 and img[0].tobytes() == to_remove[0].tobytes():
            print("eq")
        else:
            print("bad")

        if len(to_remove) != 0:
            os.remove(to_remove[1])
        to_remove = img

except KeyboardInterrupt:
    if len(to_remove) != 0:
        os.remove(to_remove[1])
    dirs = os.listdir()
    for dir in dirs:
        if os.path.isdir(dir) and dir[0].isalpha():
            print(dir)
            os.removedirs(dir)
