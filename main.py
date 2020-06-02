from screenshoter import ScreenShoter, ScreenFromTime
from hotkeyer import KeyListener

from_time = ScreenFromTime(ScreenShoter("time"), 3)
from_key = KeyListener(ScreenShoter("key"))

from_key.screen_shoter.get_area()
from_key.screen_shoter.fix_coord()

from_key.start()

from_time.start()

while True:
    img = ScreenShoter.queue.get()
    img[0].save(img[1])
    print(f"{img[1]} saved")