
class CmdResponse:
    __status: bool
    __type: str
    __data: dict
    __content: str

    def __init__(self, status: bool, contentType: str):
        self.__status = status
        self.__type = contentType
        self.__data = {'status': status}
        self.__content = None

    def setData(self, data: object):
        self.__data['data'] = data

    def setContent(self, content: str):
        self.__content = content

    def getContent(self) -> str:
        return self.__content

    def getData(self) -> dict:
        return self.__data

    def getContentType(self) -> str:
        return self.__type

    def getStatus(self) -> bool:
        return self.__status
