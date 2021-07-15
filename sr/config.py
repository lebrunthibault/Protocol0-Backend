from os.path import dirname, realpath

root = dirname(realpath(__file__))


class Config:
    TEST_DATA_DIRECTORY = f"{root}/tests/data"
    TRAINING_SYNONYMS_DIRECTORY = f"{root}/training/synonyms"
    TRAINING_AUDIO_DIRECTORY = f"{root}/training/audio"
    SYNONYMS_PATH = f"{root}/dictionary/synonyms.py"
    KALDI_VOCABULARY_PATH = f"{root}/grammar/vocabulary.txt"
