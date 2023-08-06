from datetime import date


class Date:
    __date: date
    __format: str

    def __init__(self, val: date, dateFormat: str):
        self.__date = val
        self.__format = dateFormat

    def getValue(self) -> date:
        return self.__date

    def toString(self) -> str:
        return self.__date.strftime(self.__format)
