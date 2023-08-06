import logging
import argparse

from pathlib import Path


class ParseLoggingArgument(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = getattr(logging, values.upper())
        setattr(namespace, self.dest, values)

class ParsePathArgument(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = Path(values)
        setattr(namespace, self.dest, values)

class ParsePathResolvedArgument(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = Path(values).resolve()
        setattr(namespace, self.dest, values)

class ArgsManager():
    def __init__(self, prog:str, description:str = None):
        self.parser = argparse.ArgumentParser(prog=prog, description=description)

    def _add_logging_arguments(self, parser, default_lvl=logging.WARNING):
        parser.add_argument("--log", type=str, default=default_lvl, action=ParseLoggingArgument,
            choices=["critical", "error", "warning", "info", "debug"],
            help="Level of console logger."
        )

    def get_parser(self) -> argparse.ArgumentParser:
        # self._add_logging_arguments(self.parser)
        return self.parser

    def parse_arguments(self, args) -> argparse.Namespace:
        return self.parser.parse_args(args)
