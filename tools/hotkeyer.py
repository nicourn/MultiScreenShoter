from pynput import keyboard
from threading import Thread


class KeyListener(Thread):
    def __init__(self, shoter):
        Thread.__init__(self, daemon=True)
        self.combinations = [{keyboard.Key.shift, keyboard.KeyCode(char='s')},
                             {keyboard.Key.shift, keyboard.KeyCode(char='S')}]
        self.current = set()
        self.screen_shoter = shoter

    def on_press(self, key):
        if any([key in COMBO for COMBO in self.combinations]):
            self.current.add(key)
            if any(all(k in self.current for k in COMBO) for COMBO in self.combinations):
                self.screen_shoter.take_screen(f"{self.screen_shoter.id}_"
                                               f"{self.screen_shoter.prefix}"
                                               f"{self.screen_shoter.num}.bmp")

    def on_release(self, key):
        if any([key in COMBO for COMBO in self.combinations]):
            try:
                self.current.remove(key)
            except:
                print("err")

    def run(self) -> None:
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
