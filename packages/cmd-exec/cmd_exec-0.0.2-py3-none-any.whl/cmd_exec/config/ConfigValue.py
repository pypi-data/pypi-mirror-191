
class ConfigValue:
    __value: object

    def __init__(self, value: object):
        self.__value = value

    def isNull(self) -> bool:
        return self.__value is None

    def getValue(self) -> object:
        return self.__value

    def getValueAsStr(self) -> str:
        return str(self.__value)

    def isDict(self) -> bool:
        return isinstance(self.__value, dict)

    def isList(self) -> bool:
        return isinstance(self.__value, list)

    def isInt(self) -> bool:
        return isinstance(self.__value, int)

    def isString(self) -> bool:
        return isinstance(self.__value, str)

    def hasTypeMismatch(self, value: 'ConfigValue'):
        return type(self.__value) is not type(value.getValue())

    def appendValue(self, configValue: 'ConfigValue'):
        if self.hasTypeMismatch(configValue):
            raise Exception('Type does not match')
        elif self.isDict():
            self.__value.update(configValue.getValue())
        elif self.isInt():
            self.__value += configValue.getValue()
        elif self.isList():
            self.__value += configValue.getValue()
        elif self.isString():
            self.__value += configValue.getValue()
