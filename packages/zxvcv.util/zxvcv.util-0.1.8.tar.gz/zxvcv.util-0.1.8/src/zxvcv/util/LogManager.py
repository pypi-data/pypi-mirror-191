import logging

from enum import Enum
from pathlib import Path


class LogFormatter(Enum):
    DEFAULT_LONG = r"%(asctime)s - %(name)s - %(levelname)-8s - %(message)s"
    DEFAULT_SHORT = r"[%(levelname)-8s]:%(message)s"

class LogManager():
    @staticmethod
    def setup_logger(name:str, level:int=logging.WARNING, console:bool = True,
                     file:Path = None,
                     console_format:str = LogFormatter.DEFAULT_SHORT,
                     file_format:str = LogFormatter.DEFAULT_LONG) -> logging.Logger:
        """Setup logger for given name (target).

        Args:
            name (str): Name of the logger to setup.
            level (int, optional): Level of the console logging level. Defaults to logging.WARNING.
            console (bool, optional): If True logger will be printing messages to the console.
                Defaults to True.
            file (Path, optional): Path to the directory where .log file will be stored
                (file name will be <name>.log). Defaults to None.
            template (str, optional): template how logs should be printed out.

        Returns:
            logging.Logger: Logger that have been setuped.
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if type(console_format) == LogFormatter:
            console_format = console_format.value
        if type(file_format) == LogFormatter:
            file_format = file_format.value

        if file:
            file.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(file/f"{name}.log", encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(file_format))
            logger.addHandler(file_handler)

        if console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(logging.Formatter(console_format))
            logger.addHandler(console_handler)

        if not file and not console:
            logger.disabled = True

        return logger
