from screenshoter import ScreenShoter, ScreenFromTime
from hotkeyer import KeyListener
import os

from_time = ScreenFromTime(ScreenShoter("time", "time/"), 3)
from_key = KeyListener(ScreenShoter("key", "key/"))

from_key.screen_shoter.get_area()
from_key.screen_shoter.fix_coord()

from_key.start()

from_time.start()

try:
    while True:
        img = ScreenShoter.queue.get()
        # Пересылка изображения
        img[0].save(img[1])
        print(f"{img[1]} saved")

        os.remove(img[1])
        print(f"{img[1]} deleted")
except KeyboardInterrupt:
    dirs = os.listdir()
    for dir in dirs:
        if os.path.isdir(dir) and dir[0].isalpha():
            print(dir)
            os.removedirs(dir)
