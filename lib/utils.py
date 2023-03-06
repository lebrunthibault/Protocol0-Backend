import json
import subprocess
import time
from json import JSONDecodeError
from typing import Optional, Dict

import mido
from loguru import logger
from protocol0.domain.shared.errors.Protocol0Error import Protocol0Error

from protocol0.application.command.SerializableCommand import SerializableCommand


def filename_datetime() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def copy_to_clipboard(data: str):
    subprocess.run("clip", universal_newlines=True, input=data)


def log_string(string) -> str:
    return str(string).replace("<", "\\<")


def make_sysex_message_from_command(command: SerializableCommand) -> mido.Message:
    assert isinstance(command, SerializableCommand), (
        "expected SerializableCommand, got %s" % command
    )
    message = command.serialize()
    b = bytearray(message.encode())
    b.insert(0, 0xF0)
    b.append(0xF7)
    return mido.Message.from_bytes(b)


def make_script_command_from_sysex_message(message: mido.Message) -> Optional[SerializableCommand]:
    dict = make_dict_from_sysex_message(message)
    if dict is None:
        return None
    try:
        return SerializableCommand.un_serialize(json.dumps(dict))
    except (AssertionError, Protocol0Error):
        return None


def make_dict_from_sysex_message(message: mido.Message) -> Optional[Dict]:
    if message.is_cc(121) or message.is_cc(123):
        # logger.debug("skipping cc 121 or 123")
        return None
    string: str = message.bin()[1:-1].decode("utf-8")
    if not string.startswith("{"):
        return None
    try:
        return json.loads(string)
    except JSONDecodeError:
        logger.error(f"json decode error on string : {string}, message: {message}")
        return None
