from typing import List

import PySimpleGUI as sg
from PySimpleGUI import Button, BLUES

from gui.window.decorators.close_window_on_end_decorator import CloseWindowOnEndDecorator
from gui.window.select.button_colors import ButtonColors
from gui.window.select.select import Select
from gui.window.window import Window
from gui.window.window_factory import WindowFactory
from lib.enum.color_enum import ColorEnum


class SelectFactory(WindowFactory):
    @classmethod
    def createWindow(cls, message: str, options: List, vertical: bool, color: ColorEnum) -> Window:
        button_colors = cls._get_button_color(color)
        buttons = cls._create_buttons(options, button_colors)

        kwargs = {
            "message": message,
            "options": options,
            "button_colors": button_colors,
            "background_color": color,
        }

        if vertical:
            select = Select(
                buttons=[[button] for button in buttons], arrow_keys=("Up", "Down"), **kwargs  # type: ignore[arg-type]
            )
        else:
            select = Select(buttons=[buttons], arrow_keys=("Left", "Right"), **kwargs)  # type: ignore[arg-type]

        return CloseWindowOnEndDecorator(select)

    @classmethod
    def _get_button_color(cls, color: ColorEnum) -> ButtonColors:
        if color == ColorEnum.INFO:
            return ButtonColors(BLUES[1], BLUES[0])
        elif color == ColorEnum.ERROR:
            return ButtonColors("#91403d", color.hex_value)
        else:
            return ButtonColors(color.hex_value, color.hex_value)

    @classmethod
    def _create_buttons(self, options: List[str], colors: ButtonColors) -> List[Button]:
        return [
            sg.Button(
                option,
                key=option,
                enable_events=True,
                button_color=("white", colors.selected_color) if i == 0 else colors.default_color,
            )
            for i, option in enumerate(options)
        ]
