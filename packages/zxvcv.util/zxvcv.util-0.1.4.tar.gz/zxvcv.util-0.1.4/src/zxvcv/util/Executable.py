import logging
import subprocess

from typing import List
from pathlib import Path

# from .ADict import ADict
from zxvcv.util.Path import context_cwd

log = logging.getLogger(__name__)


class Executable():
    _EXE = None

    @classmethod
    def _execute(cls, cmd:List[str], workplace:Path=Path.cwd()) -> subprocess.CompletedProcess:
        cmd_output = None
        with context_cwd(workplace):
            cmd_output = subprocess.run(
                [cls._EXE] + cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        log.debug(cmd_output)
        return cmd_output
