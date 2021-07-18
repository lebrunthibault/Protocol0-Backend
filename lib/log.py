import json
import sys

from loguru import logger

from config import LOGGING_DIRECTORY, PROJECT_ROOT


def configure_logging(filename: str) -> None:
    with open(f"{PROJECT_ROOT}/lib/logging_config.json") as config_file:
        logging_config = json.load(config_file)

    logger.remove()
    logger.add(
        sys.stdout,
        level=logging_config.get("level"),
        format=logging_config.get("format_stdout"),
    )

    logger.add(
        f"{LOGGING_DIRECTORY}\\{filename}",
        level=logging_config.get("level"),
        format=logging_config.get("format_log_file"),
        colorize=True
    )