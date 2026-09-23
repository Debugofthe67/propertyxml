import plistlib
from pathlib import Path

class PlistHandler:
    @staticmethod
    def load(file_path):
        """
        Loads a property list file (XML, binary, or text/OpenStep) 
        and returns its contents as a Python dictionary or list.
        """
        path = Path(file_path)
        with path.open("rb") as fp:
            return plistlib.load(fp)

    @staticmethod
    def save(data, file_path, as_binary=True):
        """
        Saves a Python dictionary/list back to a property list file on disk.
        Defaults to binary format (`FMT_BINARY`), falling back to XML (`FMT_XML`) if specified.
        """
        path = Path(file_path)
        fmt = plistlib.FMT_BINARY if as_binary else plistlib.FMT_XML
        with path.open("wb") as fp:
            plistlib.dump(data, fp, fmt=fmt)
