from typing import Dict
from enum import Enum

from ..ADict import ADict


class FileStatus(Enum):
    UNMODIFIED      = " "
    MODIFIED        = "M"
    TYPE_CHANGED    = "T"
    ADDED           = "A"
    DELETED         = "D"
    RENAMED         = "R"
    COPIED          = "C"
    UPDATED         = "U"
    UNTRACKED       = "?"
    IGNORED         = "!"
    # UNKNOWN         = ""

    @staticmethod
    def get_status(index_status, wtree_status) -> Dict[str, "FileStatus"]:
        return ADict({
            "index": FileStatus(index_status),
            "wtree": FileStatus(wtree_status)
        })
