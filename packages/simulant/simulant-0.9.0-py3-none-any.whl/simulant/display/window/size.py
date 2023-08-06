from ...os import Shell


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
        self.execute(f"xdotool windowsize --sync {self.window_id} {value} {self.height}")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self.execute(f"xdotool windowsize --sync {self.window_id} {self.width} {value}")
        self._height = value

    def set(self, width, height):
        self.execute(f"xdotool windowsize --sync {self.window_id} {width} {height}")
        self._width = width
        self._height = height

    def __str__(self):
        return f"width: {self.width}, height: {self.height}"

    def __repr__(self):
        return self.__str__()
