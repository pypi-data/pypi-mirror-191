
class File:
    _path: list

    def __init__(self, path: list = []):
        self._path = path

    def toString(self) -> str:
        return str(self._path)

