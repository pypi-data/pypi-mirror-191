import subprocess
import sys
import pytesseract

from build.lib.simulant.os import Shell
from .display import Display
from .keyboard import Keyboard
from .keyboard.key import keys
from .mouse import Mouse

__all__ = ['sm', 'keys']


class Simulant(Shell):
    def __init__(self):
        self.os = sys.platform
        self.keyboard = Keyboard()
        self.display = Display()
        self.mouse = Mouse()

    @staticmethod
    def get_clipboard():
        return subprocess.check_output(["xclip", "-o"]).decode('utf-8')

    def get_window_by_id(self, window_id):
        return self.display.screen(0).get_window_by_id(window_id)

    def get_window_by_name(self, window_name):
        return self.display.screen(0).get_window_by_name(window_name)


    def screenshot(self, position_x=0, position_y=0, width=None, height=None):
        return self.display.screenshot(position_x, position_y, width, height)

    def read_text(self, position_x, position_y, width, height):
        image = self.screenshot(position_x, position_y, width, height)
        string = pytesseract.image_to_string(image)
        return string

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<Simulant: {self.os}>"


sm = Simulant()
