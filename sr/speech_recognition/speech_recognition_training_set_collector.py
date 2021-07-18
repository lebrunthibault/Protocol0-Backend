import os
from os.path import exists

from lib.utils import filename_datetime
from sr.enums.ableton_command_enum import AbletonCommandEnum
from sr.enums.recognizer_step_enum import RecognizerStepEnum
from sr.recognizer.recognizer import RecognizerResult
from sr.speech_recognition.abstract_speech_recognition import AbstractSpeechRecognition
from sr.sr_config import SRConfig


class SpeechRecognitionTrainingSetCollector(AbstractSpeechRecognition):
    def __init__(self, target_word: str):
        super().__init__()
        assert (
                target_word == "noise" or target_word in AbletonCommandEnum.words()
        ), "word should be 'noise' or in the word enum"
        self._target_word = target_word
        self.recognizer.final_recognizer_step = RecognizerStepEnum.NO_PROCESSING
        self.recognizer.subscribe(RecognizerResult, self._export_recognizer_result)

    def _export_recognizer_result(self, recognizer_result: RecognizerResult):
        """ Export recording to appropriate directory for training """
        sample_subdir = "noise" if self._target_word == "noise" else f"words/{self._target_word}"
        sample_directory = f"{SRConfig.TRAINING_AUDIO_DIRECTORY}/{sample_subdir}"
        if not exists(sample_directory):
            os.mkdir(sample_directory)

        recognizer_result.recording.export(f"{sample_directory}/{filename_datetime()}.wav")