import tkinter as tk
from PIL import Image, ImageTk, ImageChops
import pyscreenshot
import random
from multiprocessing import Queue
from threading import Thread
from time import sleep
from os import mkdir


class ScreenShoter():
    queue = Queue()
    areas = []
    id = random.randint(0, 1000)

    def __init__(self, prefix="", path=''):
        self.rect_id = None
        self.num = 0
        self.prefix = prefix
        self.path = path
        if len(self.path) > 0:
            mkdir(self.path)

    def take_screen(self, name=""):
        global img
        if name == "all_area.bmp":
            img = pyscreenshot.grab()
            img.save(name, "BMP")
            ScreenShoter.queue.put([img, self.path + name])
            self.num += 1
        else:
            for i, area in enumerate(ScreenShoter.areas):
                name = f"{ScreenShoter.id}_{self.prefix}_{self.num}.bmp"
                img = pyscreenshot.grab(bbox=(area[0], area[1],
                                              area[2], area[3]))
                ScreenShoter.queue.put([img, self.path + name, i])
                self.num += 1

    def add_area(self):
        path = "all_area.bmp"
        self.take_screen(path)
        index = len(ScreenShoter.areas)
        ScreenShoter.areas.append([0, 0, 0, 0])

        def get_mouse_posn(event):
            ScreenShoter.areas[index][0], ScreenShoter.areas[index][1] = event.x, event.y

        def update_sel_rect(event):
            ScreenShoter.areas[index][2], ScreenShoter.areas[index][3] = event.x, event.y
            canvas.coords(self.rect_id, ScreenShoter.areas[index][0], ScreenShoter.areas[index][1],
                          ScreenShoter.areas[index][2], ScreenShoter.areas[index][3])

        window = tk.Tk()
        window.attributes("-fullscreen", True)
        window.configure(background='grey')

        img = ImageTk.PhotoImage(Image.open(path))
        canvas = tk.Canvas(window, width=img.width(), height=img.height(),
                           borderwidth=0, highlightthickness=0)
        canvas.pack(expand=True)
        canvas.img = img
        canvas.create_image(0, 0, image=img, anchor=tk.NW)

        if self.rect_id is None:
            self.rect_id = canvas.create_rectangle(0, 0, 0, 0, dash=(2, 2), fill='', outline='white')
        else:
            print(ScreenShoter.areas[index][0], ScreenShoter.areas[index][1],
                  ScreenShoter.areas[index][2], ScreenShoter.areas[index][3])
            self.rect_id = canvas.create_rectangle(ScreenShoter.areas[index][0], ScreenShoter.areas[index][1],
                                                   ScreenShoter.areas[index][2], ScreenShoter.areas[index][3],
                                                   dash=(2, 2), fill='', outline='white')

        canvas.bind('<Button-1>', get_mouse_posn)
        canvas.bind('<B1-Motion>', update_sel_rect)
        window.bind("<Return>", lambda event: window.destroy())

        window.mainloop()

    # def print_reg(self):
    #     print(ScreenShoter.topx, ScreenShoter.topy, ScreenShoter.botx, ScreenShoter.boty)

    def fix_coord(self):
        index = len(ScreenShoter.areas) - 1
        print(index)
        print(ScreenShoter.areas[index])
        if ScreenShoter.areas[index][0] > ScreenShoter.areas[index][2]:
            ScreenShoter.areas[index][0], ScreenShoter.areas[index][2] = ScreenShoter.areas[index][2], \
                                                                         ScreenShoter.areas[index][0]
        if ScreenShoter.areas[index][1] > ScreenShoter.areas[index][3]:
            ScreenShoter.areas[index][1], ScreenShoter.areas[index][3] = ScreenShoter.areas[index][3], \
                                                                         ScreenShoter.areas[index][1]


class ScreenFromTime(Thread):
    def __init__(self, screen, time):
        Thread.__init__(self, daemon=True)
        self.screen: ScreenShoter = screen
        self.time = time

    def run(self):
        while True:
            sleep(self.time)
            self.screen.take_screen(f"{self.screen.id}_{self.screen.prefix}{self.screen.num}.bmp")
