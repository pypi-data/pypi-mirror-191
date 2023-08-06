class Panel:
    def __init__(self):
        self.height = 26  # todo: read config file

    def __str__(self):
        return f"<{self.__class__.__name__}: LXDE>"

    def __repr__(self):
        return self.__str__()
