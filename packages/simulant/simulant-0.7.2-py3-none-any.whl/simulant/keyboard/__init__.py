import random
import subprocess
from time import sleep
from .key import letters, Keys


class Keyboard:
    SHIFT_PRESS_TIMEOUT = .1
    keys = Keys()

    def type(self, text):
        codes = []
        for symbol in text:
            delay = random.uniform(.055, .22)
            if symbol.lower() in list(letters.keys()):
                letter = letters.get(symbol.lower())
                before_press = after_press = delay / 2
                if symbol.isupper():
                    sleep(self.SHIFT_PRESS_TIMEOUT)
                    subprocess.call(["xdotool", "keydown", self.keys.SHIFT])
                    sleep(before_press)
                    subprocess.call(["xdotool", "keydown", letter])
                    sleep(after_press)
                    subprocess.call(["xdotool", "keyup", letter])
                    subprocess.call(["xdotool", "keyup", self.keys.SHIFT])
                else:
                    sleep(before_press)
                    subprocess.call(["xdotool", "keydown", letter])
                    sleep(after_press)
                    subprocess.call(["xdotool", "keyup", letter])
            else:
                subprocess.call(["xdotool", "type", symbol])
                sleep(delay)

        assert all(v == 0 for v in codes)

    @staticmethod
    def key(keyboard_key, repeat=1, timeout=.1):
        if repeat > 1:
            counter = repeat
            while counter:
                subprocess.call(["xdotool", "key", keyboard_key])
                sleep(timeout)
                counter -= 1
        else:
            subprocess.call(["xdotool", "key", keyboard_key])
