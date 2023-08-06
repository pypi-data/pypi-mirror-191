from Xlib import display as disp
from Xlib import X
from PIL import Image

from simulant.display.panel import Panel
from simulant.display.screen import Screen
from simulant.display.utils.element import find_element
from simulant.display.utils.highlited import find_highlighted


def display_handler(f):
    def wrapper(*args):
        try:
            return f(*args)
        finally:
            args[0]._dsp.close()

    return wrapper


class Display:
    screens = []

    def __init__(self):
        self.panel = Panel()
        self.screens.append(Screen(display=self, number=0))  # todo: xdotool get all screens
        self.current_screen = self.screens[0]

    def screen(self, number):
        return [i for i in self.screens if i.number == number][0]

    @property
    @display_handler
    def width(self):
        scr = self._dsp.screen()
        width = scr.width_in_pixels
        return width

    @property
    @display_handler
    def height(self):
        scr = self._dsp.screen()
        height = scr.height_in_pixels
        return height

    @display_handler
    def screenshot(self, position_x=0, position_y=0, width=None, height=None):
        image = None
        scr = self._dsp.screen()
        width = width if width else scr.width_in_pixels
        height = height if height else scr.height_in_pixels
        root = scr.root
        raw = root.get_image(position_x, position_y, width, height, X.ZPixmap, 0xffffffff)
        image = Image.frombytes("RGB", (width, height), raw.data, "raw", "BGRX")
        return image

    @staticmethod
    def find_element(template, screanshot):
        return find_element(template, screanshot)

    @staticmethod
    def find_highlighted(before, after):
        return find_highlighted(before, after)

    @property
    def _dsp(self):
        self.__dsp = disp.Display()
        return self.__dsp
