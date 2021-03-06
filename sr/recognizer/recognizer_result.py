import json
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from lib.enum.NotificationEnum import NotificationEnum
from lib.utils import filename_datetime
from sr.audio.speech_sound import SpeechSound
from sr.enums.speech_command_enum import SpeechCommandEnum
from sr.errors.abstract_recognizer_not_found_error import AbstractRecognizerNotFoundError
from sr.sr_config import SRConfig


@dataclass(frozen=True, repr=False)
class RecognizerResult:
    speech_sound: SpeechSound
    word: Optional[str] = None
    word_enum: Optional[Enum] = None
    error: Optional[AbstractRecognizerNotFoundError] = None

    def __repr__(self):
        if self.word_enum:
            return self.word_enum.name
        elif self.word:
            return self.word
        elif self.error:
            return str(self.error)
        else:
            return "Empty RecognizerResult"

    def to_dict(self):
        return {
            "speech_sound": self.speech_sound.to_dict(),
            "result": {
                "word": self.word,
                "word_enum": self.word_enum.name if self.word_enum else "",
                "error": str(self.error),
            },
        }

    @property
    def is_activation_command(self):
        return self.word_enum in [SpeechCommandEnum.PROTOCOL, SpeechCommandEnum.EXIT]

    @property
    def notification_type(self) -> NotificationEnum:
        if self.error:
            return NotificationEnum.ERROR
        elif self.word_enum == SpeechCommandEnum.EXIT:
            return NotificationEnum.WARNING
        else:
            return NotificationEnum.SUCCESS


def export_recognizer_result(recognizer_result: RecognizerResult) -> None:
    parent_dir = "success" if recognizer_result.word_enum else "failure"
    filename = f"{SRConfig.TRAINING_AUDIO_DIRECTORY}\\raw\\{parent_dir}\\{filename_datetime()}.wav"
    recognizer_result.speech_sound.export(filename)
    with open(filename.replace(".wav", ".json"), "w") as f:
        f.write(json.dumps(recognizer_result.to_dict(), indent=4))
