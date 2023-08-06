
class ConfigKey:
    __key: str

    def __init__(self, key: str = ""):
        self.__key = key

    def isAddKey(self) -> bool:
        return self.__key.startswith('(+)')

    def getKey(self) -> str:
        if self.isAddKey():
            return self.__key[3:]
        else:
            return self.__key

    def getRawKey(self) -> str:
        return self.__key

    def isValidKey(self) -> bool:
        key = self.getKey()
        return key != ''
