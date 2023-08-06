import re
import subprocess

from .human import wind_mouse


class Mouse:

    @property
    def current_position(self):
        current = subprocess.check_output(["xdotool", "getmouselocation"]).decode('utf-8')
        x, y = re.findall(r'x:(\d+) y:(\d+) ', current)[0]
        return {"x": int(x), "y": int(y)}

    def _move(self, x, y):
        subprocess.call(["xdotool", "mousemove", str(x), str(y)])

    def move(self, x, y):
        current = self.current_position
        wind_mouse(*current.values(), x, y, move_mouse=self._move)

    @staticmethod
    def click():
        subprocess.call(["xdotool", "click", "1"])
