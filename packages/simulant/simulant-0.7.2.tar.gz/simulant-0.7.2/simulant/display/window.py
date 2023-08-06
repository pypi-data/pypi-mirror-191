import re
from time import sleep

from simulant.os import Shell
from simulant.keyboard.key import keys


class Location(Shell):
    def __init__(self, window_id, x=None, y=None):
        self.window_id = window_id
        self._x = 0
        self._y = 0
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class Size(Shell):
    def __init__(self, window_id, width=None, height=None):
        self.window_id = window_id
        self._width = 0
        self._height = 0
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    def set(self, width, height):
        self.execute(f"xdotool windowsize {self.window_id} {width} {height}")
        self.width = width
        self.height = height


class Window(Shell):
    def __init__(self, screen, id, location_x=None, location_y=None, width=None, height=None):
        self.id = id
        self._screen = screen
        self.focus()  # todo focus unfocused
        self.location = Location(self.id, location_x, location_y)
        self.size = Size(self.id, width, height)
        self._update_geometry()

    def screenshot(self, x=None, y=None, width=None, height=None):
        return self._screen._display.screenshot(x, y, width, height)

    def is_focus(self):
        output = self.execute("xdotool getwindowfocus")
        return output == self.id

    def focus(self):
        self.execute(f"xdotool windowactivate {self.id}")
        self.execute(f"xdotool windowfocus {self.id}")
        sleep(.5)

    position_pattern = re.compile(r"^Position: (\d+),(\d+) \(screen: (\d+)\)$")
    geometry_pattern = re.compile(r"^Geometry: (\d+)x(\d+)$")

    def _update_geometry(self):
        output = self.execute(f"xdotool getwindowgeometry {self.id}")
        _, position, geometry = output
        position_result = re.search(self.position_pattern, position)
        geometry_result = re.search(self.geometry_pattern, geometry)
        self.screen = int(position_result.group(3))
        self.location.x = int(position_result.group(1))
        self.location.y = int(position_result.group(2))
        self.size.width = int(geometry_result.group(1))
        self.size.height = int(geometry_result.group(2))

    def close(self):
        self.focus()
        self.execute(f"xdotool key {keys.ALT + keys.F4}")

    @property
    def name(self):
        return self.execute(f'xdotool getwindowname {self.id}')

    def __str__(self):
        return f"<Window: {self.name}>"

    def __repr__(self):
        return self.__str__()
