from ...os import Shell

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
        self.execute(f"xdotool windowmove --sync {self.window_id} {value} {self.y}")
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self.execute(f"xdotool windowmove --sync {self.window_id} {self.x} {value}")
        self._y = value

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"

    def __repr__(self):
        return self.__str__()
