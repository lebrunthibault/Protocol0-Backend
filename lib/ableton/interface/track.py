from time import sleep
from typing import List, Union, Optional

import pyautogui

from api.client.p0_script_api_client import p0_script_client
from api.settings import Settings, DOWN_BBOX
from gui.celery import notification_window
from lib.ableton.get_set import get_ableton_windows
from lib.ableton.interface.coords import Coords
from lib.ableton.interface.pixel import (
    get_pixel_color_at,
    get_coords_for_color,
    get_pixel_having_color,
)
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.decorators import timeit
from lib.enum.notification_enum import NotificationEnum
from lib.explorer import drag_file_to
from lib.mouse.mouse import click
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)

settings = Settings()


def get_focused_track_coords(box_boundary="left") -> Coords:
    x, y = get_coords_for_color(
        [PixelColorEnum.ELEMENT_FOCUSED, PixelColorEnum.ELEMENT_SELECTED],
        bbox=(40, 45, 1870, 110),
        from_right=box_boundary == "right",
    )
    p0_script_client().dispatch(EmitBackendEventCommand("track_focused"))

    return x, y + 5  # drag works better here


@timeit
def click_context_menu(track_coords: Coords, y_offsets: Union[int, List[int]]) -> Optional[Coords]:
    y_offsets = [y_offsets] if isinstance(y_offsets, int) else y_offsets

    click(track_coords, button=pyautogui.RIGHT)

    x, y = track_coords

    separator_coords_list = []

    for y_offset in y_offsets:
        # left and right
        separator_coords_list += [(x - 10, y + y_offset), (x + 10, y + y_offset)]

    separator_coords = get_pixel_having_color(separator_coords_list, is_black=True, debug=False)

    if separator_coords is None:
        notification_window.delay(
            "context menu not detected (separator)",
            NotificationEnum.WARNING.value,
            auto_close_duration=0.5,
        )
        return (0, 0)

    x_separator, y_separator = separator_coords
    menu_coords = (x_separator, y_separator + 10)

    if get_pixel_color_at(menu_coords) != PixelColorEnum.context_menu_background():
        notification_window.delay(
            "context menu not detected (background)",
            NotificationEnum.WARNING.value,
            auto_close_duration=0.5,
        )
        return (0, 0)

    click(menu_coords)

    return menu_coords


def flatten_track():
    track_coords = get_focused_track_coords()

    freeze_coords = click_context_menu(track_coords, [98, 136, 137])

    if freeze_coords is None:
        return

    sleep(0.2)

    # wait for track freeze
    while "Freeze..." in get_ableton_windows():
        sleep(0.2)

    sleep(0.3)

    click(track_coords, button=pyautogui.RIGHT)
    click((freeze_coords[0], freeze_coords[1] + 20))  # flatten track

    p0_script_client().dispatch(EmitBackendEventCommand("track_flattened"))


def load_instrument_track(instrument_name: str):
    track_path = f"{settings.ableton_set_directory}\\{settings.instrument_tracks_folder}\\{instrument_name}.als"

    drag_file_to(
        track_path,
        get_focused_track_coords(box_boundary="right"),
        bbox=DOWN_BBOX,
        drag_duration=0.2,
    )

    p0_script_client().dispatch(EmitBackendEventCommand("instrument_loaded"))


def click_focused_track():
    coords = get_focused_track_coords(box_boundary="right")
    click(coords)
    p0_script_client().dispatch(EmitBackendEventCommand("track_clicked"))
