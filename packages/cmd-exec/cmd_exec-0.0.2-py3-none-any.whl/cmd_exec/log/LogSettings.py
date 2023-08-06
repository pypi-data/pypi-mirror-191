from ..util.DataUtil import DataUtil
from ..util.FileUtil import FileUtil


class LogSettings:
    _level: str
    _dirPath: str
    _fileName: str
    _maxSize: str
    _msgFormat: str
    _dateFormat: str

    def __init__(self, values: dict):
        self.__setDefaultValues()
        if values is not None:
            self._level = DataUtil.getDefaultIfNone(values.get('level'), self._level)
            self._dirPath = DataUtil.getDefaultIfNone(values.get('dir_path'), self._dirPath)
            self._fileName = DataUtil.getDefaultIfNone(values.get('file_name'), self._fileName)
            self._maxSize = DataUtil.getDefaultIfNone(values.get('max_size'), self._maxSize)
            self._msgFormat = DataUtil.getDefaultIfNone(values.get('msg_format'), self._msgFormat)
            self._dateFormat = DataUtil.getDefaultIfNone(values.get('date_format'), self._dateFormat)

    # Getter Methods

    def getLevel(self) -> str:
        return self._level

    def getMsgFormat(self) -> str:
        return self._msgFormat

    def getDateFormat(self) -> str:
        return self._dateFormat

    def getFilePath(self, version: int = None):
        path = FileUtil.getAbsolutePath(['{dirPath}', '{fileName}.log'])
        return path.format(dirPath=self._dirPath, fileName=self._fileName)

    def getVersionFilePath(self, version: int):
        path = FileUtil.getAbsolutePath(['{dirPath}', '{fileName}_{version}.log'])
        return path.format(dirPath=self._dirPath, fileName=self._fileName, version=version)

    def getMaxSizeBlockSize(self) -> str:
        arr: list = self._maxSize.split(' ')
        return arr[1]

    def getMaxSize(self) -> int:
        arr: list = self._maxSize.split(' ')
        return int(arr[0])

    # Private Methods

    def __setDefaultValues(self):
        self._level = 'info'
        self._dirPath = 'logs'
        self._fileName = 'main'
        self._maxSize = '1 MB'
        self._msgFormat = '{level} : {msg}'
        self._dateFormat = '%Y-%m-%d %H:%M:%S'
