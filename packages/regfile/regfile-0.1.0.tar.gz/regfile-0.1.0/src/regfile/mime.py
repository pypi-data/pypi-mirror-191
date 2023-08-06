"""
Type detection for reg types

Yes I know what [MIME](https://en.wikipedia.org/wiki/MIME) means.
"""
from __future__ import annotations
from abc import ABC, abstractmethod

from .common import escape


class MIME(ABC):
    """
    Abstract base class for type detection.
    """
    mime: str

    @classmethod
    @abstractmethod
    def is_type_of(cls, value: str) -> bool:
        "Check if value is of this type."

    @classmethod
    @abstractmethod
    def mime_remove(cls, value: str) -> str:
        "Remove characteristics associated with the type"

    @classmethod
    @abstractmethod
    def mime_add(cls, value: str) -> str:
        "Re-add characteristics associated with the type"


class MIMEExact(MIME):
    """
    Tries to exactly match a string before the colon.
    """
    @classmethod
    def is_type_of(cls, value: str) -> bool:
        return value.split(":")[0] == cls.mime

    @classmethod
    def mime_remove(cls, value: str) -> str:
        return value[len(cls.mime) + 1:]

    @classmethod
    def mime_add(cls, value: str) -> str:
        return f"{cls.mime}:{value}"


class MIMEQuoted(MIME):
    """
    Checks if the string is quoted.
    """
    @classmethod
    def is_type_of(cls, value: str) -> bool:
        return (value.startswith(cls.mime) and value.endswith(cls.mime))

    @classmethod
    def mime_remove(cls, value: str) -> str:
        return value[len(cls.mime):-len(cls.mime)]

    @classmethod
    def mime_add(cls, value: str) -> str:
        return escape(value)
