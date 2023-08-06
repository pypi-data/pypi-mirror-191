import logging
import subprocess

from typing import Dict
from pathlib import Path

from zxvcv.util.Path import context_cwd
from ..ADict import ADict
from ..Executable import Executable
from .FileStatus import FileStatus

log = logging.getLogger(__name__)


class Git(Executable):
    _EXE = "git"

    @classmethod
    def status(cls, workplace=Path.cwd()) -> Dict[Path, ADict]:
        _FIELDSEPARATOR = " "

        cmd_output = Git._execute(
            cmd=[ "status", "--porcelain", "-u" ],
            workplace=workplace
        )

        parsed_result = ADict()
        for line in cmd_output.stdout.decode("utf-8").splitlines():
            status, _, fpath = line.rpartition(_FIELDSEPARATOR)
            status = line[:2]
            fpath = Path(fpath.strip())
            parsed_result[fpath] = [status[0], status[1] if len(status) == 2 else " "]

        for key, value in parsed_result.items():
            parsed_result[key] = FileStatus.get_status(value[0], value[1])

        return parsed_result

    @classmethod
    def checkout(cls, item, workplace=Path.cwd()) -> None:
        cmd_output = Git._execute(
            cmd=[ "checkout", item ],
            workplace=workplace
        )

        if cmd_output.stderr:
            stderr = cmd_output.stderr.decode("utf-8")
            for ln in stderr.splitlines():
                if "Switched to branch" in ln:
                    log.info(ln)

    @classmethod
    def pull(cls, workplace=Path.cwd()) -> None:
        cmd_output = Git._execute(
            cmd=[ "pull" ],
            workplace=workplace
        )

        if cmd_output.stdout:
            stdout = cmd_output.stdout.decode("utf-8")
            for ln in stdout.splitlines():
                # TODO[PP]: print brief information about pulled changes
                pass
