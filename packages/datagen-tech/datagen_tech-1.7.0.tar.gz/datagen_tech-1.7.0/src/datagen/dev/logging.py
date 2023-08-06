import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import appdirs

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    dir_path = appdirs.user_log_dir(appname=".datagen")
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    log_file_path = Path(dir_path + "datagen.log")
    log_file_path.touch(exist_ok=True)
    file_handler = TimedRotatingFileHandler(filename=log_file_path, when="midnight")
    file_handler.setFormatter(fmt=FORMATTER)
    return file_handler


def get_logger(logger_name: str):
    logger = logging.getLogger(name=logger_name)
    logger.setLevel(level=logging.INFO)
    logger.addHandler(hdlr=get_console_handler())
    logger.addHandler(hdlr=get_file_handler())
    logger.propagate = False
    return logger
