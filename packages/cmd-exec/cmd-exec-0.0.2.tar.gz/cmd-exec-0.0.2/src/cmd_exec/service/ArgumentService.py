import sys
from ..service.AppService import AppService
from ..service.ConfigurationService import ConfigurationService


class ArgumentService(AppService):
    __arguments: dict
    __configService: ConfigurationService

    def __init__(self, configService: ConfigurationService):
        self.__configService = configService
        self.__arguments = {'mode': 'cmd'}
        self.__setArguments()

    # Getter Methods

    def getCmd(self) -> str:
        return self.__arguments.get('cmd')

    def getMode(self) -> str:
        return self.__arguments.get('mode')

    def getArgs(self) -> dict:
        return self.__arguments

    def __setArguments(self):
        args: list = sys.argv[1:]
        param: str = None
        for arg in args:
            if arg.startswith('-'):
                param = arg[1:]
            elif param is not None:
                self.__arguments[param] = arg
            else:
                param = None
