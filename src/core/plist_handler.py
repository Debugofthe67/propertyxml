import plistlib
from pathlib import Path

class PlistHandler:
    @staticmethod
    def load(file_path):
        path = Path(file_path)
        with path.open("rb") as fp:
            return plistlib.load(fp)

    @staticmethod
    def save(data, file_path, as_binary=True):
        path = Path(file_path)
        fmt = plistlib.FMT_BINARY if as_binary else plistlib.FMT_XML
        with path.open("wb") as fp:
            plistlib.dump(data, fp, fmt=fmt)
