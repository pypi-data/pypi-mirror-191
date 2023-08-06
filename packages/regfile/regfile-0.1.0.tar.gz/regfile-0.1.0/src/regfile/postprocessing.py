"""
Line postprocessing
"""
from __future__ import annotations
from abc import ABC, abstractmethod


def linelimit(line: str, limit: int = 80) -> str:
    """
    Limit a line to a certain length by adding newlines after some commas.

    >>> linelimit("aa,bb,cc,dd", limit=6)
    'aa,bb,\\ncc,dd'
    >>> linelimit('abc=01,23,45,67,89,ab,cd,ef', limit=16)
    'abc=01,23,45,\\n  67,89,ab,cd,\\n  ef'
    >>> linelimit('aaaaaaaaaa=01,23,45,67,89,ab,cd,ef', limit=10)
    'aaaaaaaaaa=01,\\n  23,45,\\n  67,89,\\n  ab,cd,\\n  ef'

    Args:
        line: The line to limit.
        limit: The maximum length of the line.

    Returns:
        The line, limited to the given length.
    """
    if "," not in line:
        return line
    res = ""
    char_count = 0
    for chars in line.split(","):
        added_chars = chars + ","
        res += added_chars
        char_count += len(added_chars)
        if char_count + len(chars) > limit - 2:
            res += "\\\n  "
            char_count = 2
    if res.endswith(","):
        res = res[:-1]
    return res


class PostProcessor(ABC):
    """
    Abstract base class for post-processing.
    """
    @staticmethod
    @abstractmethod
    def postprocess(line: str) -> str:
        """
        Postprocess a line.

        Args:
            line: The line to postprocess.

        Returns:
            The postprocessed line.
        """


class PPNone(PostProcessor):
    """
    Post-processor that does nothing.
    """
    @staticmethod
    def postprocess(line: str) -> str:
        "Returns the line as is"
        return line


class PPLinelimit(PostProcessor):
    """
    Post-processor that limits a line to ~80 characters.
    """
    @staticmethod
    def postprocess(line: str) -> str:
        "Limits the line to ~80 characters"
        return linelimit(line)
