
class ServiceProperties:
    __id: str
    __cls: str
    __args: list
    __init: bool
    __path: str
    __moduleName: str

    def __init__(self, id: str, cls: str, args: list):
        self.__id = id
        self.__cls = cls
        self.__args = []
        if args is not None:
            self.__args = args
        self.__init = False
        self.__path = None
        self.__moduleName = None

    # Getter Methods

    def getId(self) -> str:
        return self.__id

    def getClassPath(self) -> str:
        if self.__path is not None:
            return self.__path
        return 'modules.' + self.__moduleName + '.src.service.' + self.__cls

    def getArgs(self) -> list:
        retList = []
        for arg in self.__args:
            if arg == 'appConfigs':
                retList.append({'type': 'configs', 'value': arg})
            elif arg.startswith('@'):
                retList.append({'type': 'service', 'value': arg[1:]})
            else:
                retList.append({'type': 'other', 'value': arg})
        return retList

    def getClassName(self) -> str:
        classPath = self.getClassPath()
        arr = classPath.split('.')
        return arr[-1]

    def getPath(self) -> str:
        return self.__path

    def getInit(self) -> bool:
        return self.__init

    def getModuleName(self) -> str:
        return self.__moduleName

    # Setter Methods

    def setModuleName(self, name: str):
        self.__moduleName = name

    def setPath(self, path: str):
        self.__path = path

    def setInit(self, value: bool):
        self.__init = value
