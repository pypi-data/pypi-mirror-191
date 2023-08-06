from ..error.CmdExecError import CmdExecError
from ..util.FileUtil import FileUtil
from ..util.StrUtil import StrUtil


class ValidationUtil:

    @staticmethod
    def failIfDirectoryCanNotBeAccessed(path: list, code: str, params: dict = {}):
        if not FileUtil.isDirectoryReadable(path):
            raise CmdExecError(code, params)

    @staticmethod
    def failIfFileCanNotBeAccessed(path: list, code: str, params: dict = {}):
        if not FileUtil.isFileReadable(path):
            raise CmdExecError(code, params)

    @staticmethod
    def failIfStrNoneOrEmpty(val: str, code: str, params: dict = {}):
        if not isinstance(val, str) or StrUtil.isNoneOrEmpty(val):
            raise CmdExecError(code, params)

    @staticmethod
    def failIfBothStrNoneOrEmpty(values: list, code: str, params: dict = {}):
        shouldFail = True
        for value in values:
            if isinstance(value, str) and not StrUtil.isNoneOrEmpty(value):
                shouldFail = False
                break
        if shouldFail:
            raise CmdExecError(code, params)

    @staticmethod
    def failIfStringContainsChars(srcStr: str, chars: list, code: str, params: dict = {}):
        for char in chars:
            if char in srcStr:
                raise CmdExecError(code, params)

    @staticmethod
    def failIfNotType(obj: object, type, code: str, params: dict = {}):
        if not isinstance(obj, type):
            raise CmdExecError(code, params)

    @staticmethod
    def failIfClassFileDoesNotExist(clsPath: str, code: str, params: dict = {}):
        path = StrUtil.convertClassPathToFilePath(clsPath)
        if len(path) == 0 or not FileUtil.doesFileExist(path, 'py'):
            raise CmdExecError(code, params)

    @staticmethod
    def failIfNotSubClass(srcCls, type):
        if not issubclass(srcCls, type):
            raise CmdExecError('ERR59')
