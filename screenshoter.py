import tkinter as tk
from PIL import Image, ImageTk
import pyscreenshot
import random
from multiprocessing import Queue
from threading import Thread
from time import sleep


class ScreenShoter():
    queue = Queue()
    topx, topy, botx, boty = (0, 0, 0, 0)
    id = random.randint(0, 1000)

    def __init__(self, prefix=""):
        self.rect_id = None
        self.num = 0
        self.prefix = prefix

    def take_screen(self, name=""):
        global img
        if name == "all_area.bmp":
            img = pyscreenshot.grab()
            img.save(name, "BMP")
        else:
            name = f"{ScreenShoter.id}_{self.prefix}_{self.num}.bmp"
            img = pyscreenshot.grab(bbox=(ScreenShoter.topx, ScreenShoter.topy,
                                          ScreenShoter.botx, ScreenShoter.boty))
        ScreenShoter.queue.put([img, name])
        self.num += 1

    def get_area(self):
        path = "all_area.bmp"
        self.take_screen(path)

        def get_mouse_posn(event):
            ScreenShoter.topx, ScreenShoter.topy = event.x, event.y

        def update_sel_rect(event):
            ScreenShoter.botx, ScreenShoter.boty = event.x, event.y
            canvas.coords(self.rect_id, ScreenShoter.topx, ScreenShoter.topy, ScreenShoter.botx, ScreenShoter.boty)

        window = tk.Tk()
        window.attributes("-fullscreen", True)
        window.configure(background='grey')

        img = ImageTk.PhotoImage(Image.open(path))
        canvas = tk.Canvas(window, width=img.width(), height=img.height(),
                           borderwidth=0, highlightthickness=0)
        canvas.pack(expand=True)
        canvas.img = img
        canvas.create_image(0, 0, image=img, anchor=tk.NW)

        self.rect_id = canvas.create_rectangle(ScreenShoter.topx, ScreenShoter.topy, ScreenShoter.topx,
                                               ScreenShoter.topy,
                                               dash=(2, 2), fill='', outline='white')

        canvas.bind('<Button-1>', get_mouse_posn)
        canvas.bind('<B1-Motion>', update_sel_rect)
        window.bind("<Return>", lambda event: window.destroy())

        window.mainloop()

    def print_reg(self):
        print(ScreenShoter.topx, ScreenShoter.topy, ScreenShoter.botx, ScreenShoter.boty)

    def fix_coord(self):
        if ScreenShoter.topx > ScreenShoter.botx:
            ScreenShoter.topx, ScreenShoter.botx = ScreenShoter.botx, ScreenShoter.topx
        if ScreenShoter.topy > ScreenShoter.boty:
            ScreenShoter.topy, ScreenShoter.boty = ScreenShoter.boty, ScreenShoter.topy


class ScreenFromTime(Thread):
    def __init__(self, screen, time):
        Thread.__init__(self)
        self.screen: ScreenShoter = screen
        self.time = time

    def run(self):
        while True:
            sleep(self.time)
            self.screen.take_screen(f"{self.screen.id}_{self.screen.prefix}{self.screen.num}.bmp")
