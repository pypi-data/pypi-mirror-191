from ..error.ErrorMessage import ErrorMessage


class CmdExecError(Exception):
    __code: str

    def __init__(self, code: str, params: dict = {}):
        self.__code = code
        message = ErrorMessage.getMessage(code).format(**params)
        super().__init__(message)

    def getCode(self) -> str:
        return self.__code
