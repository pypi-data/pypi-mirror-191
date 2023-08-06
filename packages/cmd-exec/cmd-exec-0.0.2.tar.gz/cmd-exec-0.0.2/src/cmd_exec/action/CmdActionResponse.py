
class CmdActionResponse:
    __status: bool
    __msg: str

    def __init__(self, status: bool, msg: str):
        if isinstance(status, bool):
            self.__status = status
        else:
            self.__status = False
        self.__msg = msg

    def isSuccess(self) -> bool:
        return self.__status is True

    def isFail(self) -> bool:
        return self.__status is False

    def getMsg(self) -> str:
        return self.__msg
