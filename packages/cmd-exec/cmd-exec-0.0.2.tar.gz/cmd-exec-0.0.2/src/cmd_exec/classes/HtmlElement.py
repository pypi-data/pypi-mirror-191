
class HtmlElement:
    __tag: str
    __attrs: dict
    __data: str
    __children: list
    __parent: object

    def __init__(self, tag: str, attrs: list, parent: object):
        self.__tag = tag
        self.__children = []
        self.__data = ''
        self.__setAttrs(attrs)
        self.__parent = parent

    def __setAttrs(self, attrs: list):
        self.__attrs = {}
        for val in attrs:
            self.__attrs[val[0]] = val[1]

    def addChild(self, element: object):
        self.__children.append(element)

    def addAttr(self, name: str, value: str):
        self.__attrs[name] = value

    def addData(self, data: str):
        if data is not None:
            self.__data = data.strip()

    def hasChildren(self):
        return len(self.__children) > 0

    def hasData(self) -> bool:
        return self.__data != ''

    def getTag(self) -> str:
        return self.__tag

    def getChildren(self) -> list:
        return self.__children

    def getAttrs(self) -> dict:
        return self.__attrs

    def getData(self) -> str:
        return self.__data

    def getParent(self) -> object:
        return self.__parent
