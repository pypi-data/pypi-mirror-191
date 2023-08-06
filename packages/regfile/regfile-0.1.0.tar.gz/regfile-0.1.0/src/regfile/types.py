"""
Types of data in registry files.

Data type descriptions are copied from
https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-value-types
"""
# pylint: disable=invalid-name
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from textwrap import wrap
from typing import (
    ClassVar,
    Generic,
    Optional,
    Type,
    TypeVar,
)

from .common import (
    REG_ENCODING,
    escape,
)
from .mime import (
    MIMEExact,
    MIMEQuoted,
)
from .postprocessing import (
    PPNone,
    PPLinelimit,
)


@dataclass
class RegPath:
    """
    A path to a registry key.
    """
    path: list[str]

    @classmethod
    def from_str(cls, path: str):
        """
        Create a RegPath from a string.

        Args:
            path: The path to parse.

        Returns:
            A RegPath.
        """
        return cls(path.split("\\"))

    @property
    def parent(self) -> Optional["RegPath"]:
        """
        Get the parent path.
        """
        if len(self.path) == 1:
            return None
        return RegPath(self.path[:-1])

    def __getitem__(self, index: int) -> str:
        return self.path[index]

    def __str__(self) -> str:
        return "\\".join(self.path)


T = TypeVar("T")


@dataclass
class Value(MIMEExact, PPNone, ABC, Generic[T]):
    """
    Generic value of a registry key.
    """
    name: str
    value: T
    name_quoted: bool = False
    typeof: ClassVar[str] = __name__

    # TODO: Find another way of doing this.
    def __init_subclass__(cls) -> None:
        "Change the newly created class's type name"
        super().__init_subclass__()
        cls.typeof = cls.__name__

    @classmethod
    def from_str(cls, name: str, value: str):
        """
        Create a Value from a string.

        Args:
            name: The name of the value.
            value: The value of the value.

        Returns:
            A Value.
        """
        name_quoted = False
        if name.startswith("\""):
            name = name[1:-1]
            name_quoted = True
        value = cls.mime_remove(value)
        return cls(name, cls.val_conv(value), name_quoted)

    @classmethod
    @abstractmethod
    def val_conv(cls, value: str) -> T:
        """
        Convert a string to the appropriate type.

        Args:
            value: The string to convert.

        Returns:
            The converted value.
        """

    @classmethod
    @abstractmethod
    def val_deconv(cls, value: T) -> str:
        """
        Convert a value to a string.

        Args:
            value: The value to convert.

        Returns:
            The converted string.
        """

    def to_str(self) -> str:
        """
        Convert the value to a string.

        Returns:
            The converted string
        """
        name = self.name
        if self.name_quoted:
            name = escape(name)
        value = self.val_deconv(self.value)
        value = self.mime_add(value)
        return self.postprocess(f"{name}={value}")

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.name}: {self.typeof} = {self.value}"


class REG_DWORD(Value):
    "A 32-bit number."
    value: int
    mime: str = "dword"

    @classmethod
    def val_conv(cls, value: str) -> int:
        return int(value, base=16)

    @classmethod
    def val_deconv(cls, value: int) -> str:
        return hex(value)[2:].zfill(8)


class REG_QWORD(Value):
    "A 64-bit number."
    value: int
    mime: str = "hex(b)"

    @classmethod
    def val_conv(cls, value: str) -> int:
        ordfix = value.split(",")
        ordfix.reverse()
        fixedval = "".join(ordfix)
        return int(fixedval, base=16)

    @classmethod
    def val_deconv(cls, value: int) -> str:
        vstr = hex(value)[2:].zfill(16)
        ordfix = wrap(vstr, 2)
        ordfix.reverse()
        return ",".join(ordfix)


class REG_SZ(MIMEQuoted, Value):
    """
    A null-terminated string.
    It's either a Unicode or an ANSI string, depending on whether you use the
    Unicode or ANSI functions.
    """
    value: str
    mime: str = "\""

    @classmethod
    def val_conv(cls, value: str) -> str:
        return value

    @classmethod
    def val_deconv(cls, value: str) -> str:
        return value


class REG_BINARY(PPLinelimit, Value):
    "Binary data in any form."
    value: bytes
    mime: str = "hex"

    @classmethod
    def val_conv(cls, value: str) -> bytes:
        vsplit = value.replace(",", "")
        return bytes.fromhex(vsplit)

    @classmethod
    def val_deconv(cls, value: bytes) -> str:
        vsplit = wrap(value.hex(), 2)
        return ",".join(vsplit)


class REG_EXPAND_SZ(PPLinelimit, Value):
    """
    A null-terminated string that contains unexpanded references to environment
    variables, for example, %PATH%. It's either a Unicode or an ANSI string,
    depending on whether you use the Unicode or ANSI functions. To expand the
    environment variable references, use the
    [ExpandEnvironmentStrings](https://learn.microsoft.com/en-us/windows/win32/api/processenv/nf-processenv-expandenvironmentstringsa)
    function.
    """
    value: str
    mime: str = "hex(2)"

    @classmethod
    def val_conv(cls, value: str) -> str:
        vbytes = REG_BINARY.val_conv(value)
        return str(vbytes, encoding=REG_ENCODING)

    @classmethod
    def val_deconv(cls, value: str) -> str:
        vbytes = bytes(value, encoding=REG_ENCODING)
        return REG_BINARY.val_deconv(vbytes)


class REG_MULTI_SZ(PPLinelimit, Value):
    """
    A sequence of null-terminated strings, terminated by an empty string (\\0).
    The following is an example:
    String1\\0String2\\0String3\\0LastString\\0\\0.
    The first \\0 terminates the first string,
    the second-from-last \\0 terminates the last string,
    and the final \\0 terminates the sequence.
    Note that the final terminator must be factored into the length of the string.
    """
    value: list[str]
    mime: str = "hex(7)"

    @classmethod
    def val_conv(cls, value: str) -> list[str]:
        res = REG_EXPAND_SZ.val_conv(value).split("\x00")
        for _ in range(2):
            res.pop(-1)
        return res

    @classmethod
    def val_deconv(cls, value: list[str]) -> str:
        for _ in range(2):
            value.append("")
        return REG_EXPAND_SZ.val_deconv("\x00".join(value))


# NOTE: Not implemented
class REG_RESOURCE_REQUIREMENTS_LIST(Value):
    value: list[str]
    mime: str = "hex(a)"

    @classmethod
    def is_type_of(cls, value: str) -> bool:
        return False

    @classmethod
    def val_conv(cls, value: str) -> list[str]:
        return []

    @classmethod
    def val_deconv(cls, value: list[str]) -> str:
        return ""


# TODO: Remove and add support for whatever this is:
# hex(ffff0011):ff
class REG_SKIP(Value):
    value: str
    mime: str = "hex(ff"

    @classmethod
    def is_type_of(cls, value: str) -> bool:
        return False

    @classmethod
    def val_conv(cls, value: str) -> str:
        return ""

    @classmethod
    def val_deconv(cls, value: str) -> str:
        return ""


mimemap: list[type[Value]] = [
    REG_DWORD,
    REG_QWORD,
    REG_EXPAND_SZ,
    REG_MULTI_SZ,
    REG_BINARY,
    REG_SZ,
]


def value_from_str(text: str) -> Value:
    """
    Returns a Value object from a string.

    Raises:
        TypeError: If the string value type could not be determined.
    """
    name: str = text.split("=")[0]
    value: str = text.split("=")[1]
    reg_type: Type[Value]
    for reg_type in mimemap:
        if not reg_type.is_type_of(value):
            continue
        res = reg_type.from_str(name, value)
        assert res is not None  # NOTE: This is a hack
        return res
    raise TypeError(f"Unknown type for line:\n{escape(text)}")


@dataclass
class Key:
    path: RegPath
    subkeys: list["Key"] = field(default_factory=list)
    values: list[Value] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.path[-1]

    @property
    def parent(self) -> Optional[RegPath]:
        return self.path.parent

    def add_subkey(self, key):
        self.subkeys.append(key)

    def __getitem__(self, name: str) -> "Key":
        for key in self.subkeys:
            if key.name == name:
                return key
        raise KeyError(name)

    def add_value(self, value: Value):
        self.values.append(value)

    def get_value(self, name: str) -> Optional[Value]:
        for value in self.values:
            if value.name == name:
                return value
        return None

    def find_key(self, path: list[str]) -> "Key":
        if len(path) < 1:
            raise ValueError()
        search = path.pop(0)
        key = self[search]
        if len(path) == 0:
            return key
        return key.find_key(path)

    def __str__(self):
        return self.path.__str__()

    def __repr__(self):
        return f"Key({self.path})"

    def dump(self) -> str:
        res = f"[{self.path}]\n"
        for value in self.values:
            res += value.to_str() + "\n"
        res += "\n"
        return res
