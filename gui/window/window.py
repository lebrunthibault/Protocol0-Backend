from functools import partial
from typing import Optional

from PySimpleGUI import Window as SgWindow

from lib.patterns.observer.subject_mixin import SubjectMixin
from lib.timer import start_timer
from lib.window.window import focus_window


class Window(SubjectMixin):
    sg_window: Optional[SgWindow] = None

    def display(self):
        raise NotImplementedError

    def focus(self):
        if self.sg_window.Title is None:
            return
        for interval in (0.5, 1):
            start_timer(interval, partial(focus_window, self.sg_window.Title))

    def is_event_escape(self, event):
        return event == "Exit" or event.split(":")[0] == "Escape"

    def is_event_enter(self, event):
        return len(event) == 1 and ord(event) == 13
