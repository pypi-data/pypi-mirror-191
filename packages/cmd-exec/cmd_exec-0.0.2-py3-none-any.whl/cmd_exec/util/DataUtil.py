
class DataUtil:
    @staticmethod
    def getDefaultIfNone(value: object, defaultValue: object) -> object:
        if value is None:
            return defaultValue
        return value
