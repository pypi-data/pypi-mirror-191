from datetime import datetime, date
from ..date.Date import Date


class DateUtil:

    @staticmethod
    def getCurrentDateTimeAsStr(formatStr: str = "%Y-%m-%d %H:%M:%S") -> str:
        now = datetime.now()
        return now.strftime(formatStr)

    @staticmethod
    def convertStrToDate(dateStr: str, dateFormat: str = '%m-%d-%Y') -> Date:
        if dateStr == 'today':
            dateObj = date.today()
        else:
            dateObj = datetime.strptime(dateStr, dateFormat)
        return Date(dateObj, dateFormat)
