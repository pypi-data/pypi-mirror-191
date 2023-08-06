"""
Parser for .reg files.
"""
# pylint: disable=invalid-name
from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
from os import (
    PathLike,
    fspath,
)
from typing import (
    Any,
    ClassVar,
    Optional,
    Tuple,
)

from .common import REG_ENCODING
from .types import (
    escape,
    RegPath,
    Value,
    value_from_str,
    Key,
)


@dataclass
class RegFileHeader:
    version: str
    has_bom: bool = False
    MIME: ClassVar[str] = "Windows Registry Editor Version {}"
    MIME_BOM: ClassVar[str] = "\ufeff"
    MIME_RE: ClassVar[str] = r"Windows Registry Editor Version (.+)"

    @classmethod
    def from_str(cls, data: str) -> "RegFileHeader":
        has_bom: bool = False
        mime = data.split("\n")[0]
        if mime[0] == cls.MIME_BOM:
            mime = mime[1:]
            has_bom = True
        match = re.match(cls.MIME_RE, mime)
        if not match:
            raise TypeError(f"""Not a registry file!
Unknown mime type: {escape(mime)}""")
        version = str(match.groups(0)[0])
        if version != "5.00":
            raise RuntimeError("Unsupported reg file version.")
        return cls(version, has_bom)

    def dump(self) -> str:
        res = self.MIME.format(self.version)
        if self.has_bom:
            res = self.MIME_BOM + res
        return res + "\n"


@dataclass
class RegFile:
    header: RegFileHeader
    keys: list[Key]
    root_key: Optional[RegPath]

    @classmethod
    def _txt_to_obj(cls, data: str) -> Tuple[RegFileHeader, list[Key]]:
        lines: list[str] = data.replace("\\\n  ", "").split("\n")
        keys: list[Key] = []
        current_key: Optional[Key] = None
        header_str: str = ""
        header: Optional[RegFileHeader] = None
        for line in lines:
            if line == "":
                continue
            if line.startswith("["):
                path = RegPath.from_str(line[1:-1])
                key = Key(path)
                keys.append(key)
                if current_key is None:
                    header = RegFileHeader.from_str(header_str)
                current_key = key
                continue
            if current_key is None:
                header_str += line + "\n"
                continue
            value: Value[Any] = value_from_str(line)
            current_key.add_value(value)
        assert header is not None
        return header, keys

    @classmethod
    def _root_detect(cls, keys: list[Key]) -> Optional[RegPath]:
        keys_without_parents = [
            key
            for key in keys
            if key.parent not in [
                key.path
                for key in keys
            ]
        ]
        if len(keys_without_parents) == 0:
            raise ValueError("Registry file has no keys.")
        elif len(keys_without_parents) == 1:
            return keys_without_parents[0].path
        return None

    @classmethod
    def from_str(cls, reg: str):
        # Stage 1 - Load file
        header, all_keys = cls._txt_to_obj(reg)
        # Stage 2 - Detect type
        # TODO: Merge _root_detect with other loops
        root_key = cls._root_detect(all_keys)
        # Stage 3 - Build tree and find root keys
        keys: list[Key] = []
        for parent in all_keys:
            # NOTE: If root_key is not none this is always false
            # TODO: Clean this up
            if parent.parent is None:
                keys.append(parent)
            for child in all_keys:
                if child.parent == parent.path:
                    parent.add_subkey(child)
        # Stage 4 - Add missing keys
        if root_key:
            tmp = all_keys[0]
            while tmp.parent:
                tmp = Key(tmp.parent)
                tmp.add_subkey(all_keys[0])
                all_keys.insert(0, tmp)
            if not keys:
                keys = [all_keys[0]]
        return cls(header, keys, root_key)

    @classmethod
    def from_path(cls, path: PathLike):
        path = Path(fspath(path))
        return cls.from_str(path.read_text(REG_ENCODING))

    def __getitem__(self, name: str) -> Key:
        for key in self.keys:
            if key.name == name:
                return key
        raise KeyError(name)

    def find_key(self, path: list[str] | str) -> Optional[Key]:
        """
        Finds key by path.
        """
        if isinstance(path, str):
            path = path.split("\\")
        search = path.pop(0)
        for key in self.keys:
            if key.name == search:
                if len(path) == 0:
                    return key
                return key.find_key(path)
        return None

    @property
    def HKEY_CLASSES_ROOT(self) -> Key:
        return self["HKEY_CLASSES_ROOT"]

    @property
    def HKEY_CURRENT_USER(self) -> Key:
        return self["HKEY_CURRENT_USER"]

    @property
    def HKEY_LOCAL_MACHINE(self) -> Key:
        return self["HKEY_LOCAL_MACHINE"]

    @property
    def HKEY_USERS(self) -> Key:
        return self["HKEY_USERS"]

    @property
    def HKEY_CURRENT_CONFIG(self) -> Key:
        return self["HKEY_CURRENT_CONFIG"]

    def dump(self) -> str:
        """
        Dump registry file to string.
        Remember that Windows's reg files use CRLF as line endings.

        Returns:
            str: Registry file as string.
        """

        res = self.header.dump() + "\n"
        if self.root_key is not None:
            root = self.find_key(str(self.root_key))
            assert root is not None
            keys = [root]
        else:
            keys = self.keys
        all_keys = []
        while keys:
            key = keys.pop(0)
            all_keys.append(key)
            keys = key.subkeys + keys
        while len(all_keys) > 0:
            key = all_keys.pop(0)
            res += key.dump()
        return res
