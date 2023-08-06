import os
import pathlib

from contextlib import contextmanager


def here(file:str) -> pathlib.PosixPath:
    """Get path of the directory of the script being run.

    Args:
        file (str): path to the file which location we want to get (usually '__file__')

    Returns:
        pathlib.PosixPath: path of the directory where script is located.
    """
    return pathlib.Path(file).parent.resolve()

@contextmanager
def context_cwd(new_cwd:pathlib.Path):
    """Change cwd for provided context

    Args:
        new_cwd (pathlib.Path): path which will be set as context cwd.
    """
    cwd = pathlib.Path.cwd()
    try:
        os.chdir(new_cwd)
        yield
    finally:
        os.chdir(cwd)

class Path(pathlib.Path):
    pass
