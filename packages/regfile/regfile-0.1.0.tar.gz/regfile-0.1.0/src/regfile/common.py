"""
Common things for regfile
"""
REG_ENCODING: str = "UTF-16LE"


def escape(text: str) -> str:
    """
    Escape a string.
    """
    return f"\"{text}\""
