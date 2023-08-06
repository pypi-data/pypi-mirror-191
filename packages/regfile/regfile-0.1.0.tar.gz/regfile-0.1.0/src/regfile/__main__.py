from pathlib import Path
from .common import REG_ENCODING
from .main import RegFile

TESTING = False


def main() -> None:
    txt = Path("/mnt/OPENCORE/reg/BTHPORT.reg").read_text(REG_ENCODING)
    res = RegFile.from_str(txt)
    target = Path("test.reg")
    if TESTING:
        ENCODING = "UTF-8"
        with open("utf.reg", "wt", encoding=ENCODING, newline="\r\n") as file:
            file.write(txt)
    else:
        ENCODING = REG_ENCODING
    target.write_text(res.dump(), encoding=ENCODING, newline="\r\n")


if __name__ == "__main__":
    main()
