
class Column:
    _title: str
    _type: str
    _isPrimary: bool

    def __init__(self, title: str, type: str, isPrimary: bool = False):
        self._title = title
        self._type = type
        self._isPrimary = isPrimary

    def getTitle(self) -> str:
        return self._title

    def getType(self) -> str:
        return self._type

    def isText(self) -> bool:
        return self._type == 'text'

    def isPrimary(self) -> bool:
        return self._isPrimary

    def isNumber(self) -> bool:
        return self._type == 'real'
