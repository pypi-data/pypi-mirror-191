
class Option:
    __id: str
    __value: str

    def __init__(self, oid: str, value: str):
        self.__id = oid
        self.__value = value

    def getValue(self) -> str:
        return self.__value

    def getId(self) -> str:
        return self.__id
