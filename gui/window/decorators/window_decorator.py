from gui.window.window import Window


class WindowDecorator(Window):
    def __init__(self, window: Window):
        self.window = window

    @property
    def sg_window(self):
        return self.window.sg_window

    def display(self):
        raise NotImplementedError
