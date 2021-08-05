from abc import abstractmethod

from typing_extensions import Protocol


class RecognizerInterface(Protocol):
    @abstractmethod
    def process_speech_sound(self):
        raise NotImplementedError

    @abstractmethod
    def load_model(self, sample_rate: int):
        raise NotImplementedError