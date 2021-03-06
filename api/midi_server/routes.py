import json
import os
import time
from typing import List, Dict

import requests
from loguru import logger

from api.client.p0_script_api_client import p0_script_client
from api.midi_server.main import notify_protocol0_midi_up, stop_midi_server
from config import Config
from gui.celery import select_window, notification_window
from lib.ableton.ableton import reload_ableton, clear_arrangement, save_set, save_set_as_template
from lib.ableton.analyze_clip_jitter import analyze_test_audio_clip_jitter
from lib.ableton.set_profiling.ableton_set_profiler import AbletonSetProfiler
from lib.decorators import reset_midi_client, throttle
from lib.enum.NotificationEnum import NotificationEnum
from lib.keys import send_keys
from lib.mouse.activate_rev2_editor import activate_rev2_editor, post_activate_rev2_editor
from lib.mouse.drum_rack import save_drum_rack
from lib.mouse.mouse import click, right_click, double_click, click_vertical_zone, move_to
from lib.mouse.toggle_ableton_button import toggle_ableton_button
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum
from lib.window.window import focus_window
from protocol0.application.command.GetSongStateCommand import GetSongStateCommand
from protocol0.application.command.PingCommand import PingCommand
from protocol0.application.command.ProcessBackendResponseCommand import (
    ProcessBackendResponseCommand,
)


class Routes:
    def test(self) -> None:
        pass

    def test_duplication(self) -> None:
        log_path = f"{Config.PROJECT_DIRECTORY}/test_duplication.txt"
        with open(log_path, "a") as f:
            f.write(f"{time.time()} - pid: {os.getpid()}\n")
        logger.info(f"pid written to {log_path}")
        os.startfile(log_path)

    @reset_midi_client
    def ping(self) -> None:
        p0_script_client().dispatch(PingCommand())

    def notify_protocol0_midi_up(self) -> None:
        notify_protocol0_midi_up()

    def get_song_state(self) -> None:
        p0_script_client().dispatch(GetSongStateCommand())

    def notify_song_state(self, state: Dict) -> None:
        """Forward to http server"""
        requests.post(f"{Config.HTTP_API_URL}/song_state", data=json.dumps(state))

    def move_to(self, x: int, y: int) -> None:
        move_to(x=x, y=y)

    def click(self, x: int, y: int) -> None:
        click(x=x, y=y)

    def click_vertical_zone(self, x: int, y: int) -> None:
        click_vertical_zone(x=x, y=y)

    def right_click(self, x: int, y: int) -> None:
        right_click(x=x, y=y)

    def double_click(self, x: int, y: int) -> None:
        double_click(x=x, y=y)

    def send_keys(self, keys: str) -> None:
        send_keys(keys)

    def select_and_copy(self) -> None:
        send_keys("^a")
        send_keys("^c")

    def select_and_paste(self) -> None:
        send_keys("^a")
        send_keys("^v")

    def analyze_test_audio_clip_jitter(self, clip_path: str):
        analyze_test_audio_clip_jitter(clip_path=clip_path)

    def show_plugins(self) -> None:
        if not find_window_handle_by_enum(
            "AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME
        ):
            send_keys("^%p")

    def show_hide_plugins(self) -> None:
        send_keys("^%p")

    def hide_plugins(self) -> None:
        if find_window_handle_by_enum(
            "AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME
        ):
            send_keys("^%p")

    def focus_window(self, window_name: str) -> None:
        focus_window(name=window_name)

    def reload_ableton(self):
        reload_ableton()

    def save_set(self):
        save_set()

    def save_set_as_template(self):
        save_set_as_template()

    def clear_arrangement(self):
        clear_arrangement()

    def toggle_ableton_button(self, x: int, y: int, activate: bool = False) -> None:
        toggle_ableton_button(x=x, y=y, activate=activate)

    def save_drum_rack(self, drum_rack_name: str) -> None:
        save_drum_rack(drum_rack_name)

    def activate_rev2_editor(self) -> None:
        activate_rev2_editor()

    def post_activate_rev2_editor(self) -> None:
        post_activate_rev2_editor()

    def start_set_profiling(self) -> None:
        AbletonSetProfiler.start_set_profiling()

    def start_profiling_single_measurement(self) -> None:
        AbletonSetProfiler.start_profiling_single_measurement()

    @reset_midi_client
    def end_measurement(self) -> None:
        AbletonSetProfiler.end_measurement()

    def stop_midi_server(self) -> None:
        stop_midi_server()

    def send_backend_response(self, res) -> None:
        p0_script_client().dispatch(ProcessBackendResponseCommand(res))

    def show_info(self, message: str, centered: bool = False):
        notification_window.delay(message, NotificationEnum.INFO.value, centered)

    def show_success(self, message: str, centered: bool = False):
        notification_window.delay(message, NotificationEnum.SUCCESS.value, centered)

    def show_warning(self, message: str, centered: bool = False):
        notification_window.delay(message, NotificationEnum.WARNING.value, centered)

    @throttle(milliseconds=5000)
    def show_error(self, message: str):
        notification_window.delay(message, NotificationEnum.ERROR.value, centered=True)

    def select(
        self,
        question: str,
        options: List,
        vertical: bool = True,
        color: str = NotificationEnum.INFO.value,
    ):
        select_window.delay(question, options, vertical, color)
