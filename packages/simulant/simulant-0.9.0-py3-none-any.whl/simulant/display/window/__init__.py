import re
from time import sleep
from ...os import Shell
from ...keyboard.key import keys
from .location import Location
from .size import Size

position_pattern = re.compile(r"^Position: (\d+),(\d+) \(screen: (\d+)\)$")
geometry_pattern = re.compile(r"^Geometry: (\d+)x(\d+)$")


class Window(Shell):
    def __init__(self, screen, id, location_x=None, location_y=None, width=None, height=None):
        self.id = id
        self._screen = screen
        self.focus()  # todo focus unfocused
        self.location = Location(self.id, location_x, location_y)
        self.size = Size(self.id, width, height)
        self._update_geometry()

    def screenshot(self, x=None, y=None, width=None, height=None):
        return self._screen._display.screenshot(
            x + self.location.x if x else self.location.x,
            y + self.location.y if y else self.location.y,
            width or self.size.width,
            height or self.size.height
        )

    def is_focus(self):
        output = self.execute("xdotool getwindowfocus")
        return output == self.id

    def focus(self):
        self.execute(f"xdotool windowactivate {self.id}")
        self.execute(f"xdotool windowfocus {self.id}")

    def _update_geometry(self):
        output = self.execute(f"xdotool getwindowgeometry {self.id}")
        _, position, geometry = output
        position_result = re.search(position_pattern, position)
        geometry_result = re.search(geometry_pattern, geometry)
        self.screen = int(position_result.group(3))
        self.location._x = int(position_result.group(1))
        self.location._y = int(position_result.group(2))
        self.size._width = int(geometry_result.group(1))
        self.size._height = int(geometry_result.group(2))

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
