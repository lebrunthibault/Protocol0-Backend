from time import sleep

from lib.ableton.ableton import is_browser_splurges_clickable, is_browser_visible
from lib.ableton_set import AbletonSet
from lib.enum.NotificationEnum import NotificationEnum
from lib.keys import send_keys, send_up, send_down, send_right, send_left
from lib.mouse.mouse import click
from gui.celery import notification_window


def search(search: str):
    send_keys("^f")
    sleep(0.1)
    send_keys(search)


def load_rev2_track():
    search('"Default.als"')
    sleep(0.2)
    send_down()
    send_down()
    send_right()

    for _ in range(12):
        send_down()

    send_up()
    send_up()

    send_keys("{ENTER}")


def load_minitaur_track():
    search('"Default.als"')
    sleep(0.2)

    send_down()
    send_down()
    send_right()

    for _ in range(12):
        send_down()

    send_up()

    send_keys("{ENTER}")


def preload_set_tracks(set: AbletonSet):
    if is_browser_visible() and not is_browser_splurges_clickable():
        notification_window.delay(
            "Browser is not selectable",
            notification_enum=NotificationEnum.WARNING.value,
            centered=True,
        )
        return

    search("")  # focus the browser
    send_keys("{BACKSPACE}")
    click(58, 500)  # click on "tracks" in browser
    sleep(0.05)
    click(86, 58)  # click in the search box without activating search mode
    sleep(0.05)

    # first writing a wrong title to clear the potential sub folder focus
    send_keys(f"{set.title}a")  # filter on the set folder
    sleep(0.2)
    send_keys("{BACKSPACE}")
    sleep(0.2)

    # a way to always show the tracks sub folder
    send_down()
    if set.has_backup:
        send_left()
        send_left()
        send_right()
        send_down()

    if set.has_freezed_samples:
        send_down()

    send_right()
    send_down()
    send_right()
    send_down()
    send_right()


def preload_sample_category(category: str):
    search("")  # focus the browser
    sleep(0.1)
    click(58, 523)  # click on samples folder in browser
    sleep(0.05)
    click(86, 58)  # click in the search box without activating search mode
    sleep(0.05)
    send_keys("^a")
    send_keys("{BACKSPACE}")
    send_keys(f"'{category}'")  # filter on the set folder
    sleep(0.2)

    # a way to always show the tracks sub folder
    send_down()

    send_right()
