from ..module.ModuleDependency import ModuleDependency
from ..module.ServiceProperties import  ServiceProperties
from ..util.ModuleUtil import ModuleUtil


class AppModule:
    __name: str
    __description: str
    __version: str
    __dependencies: list
    __services: dict

    def __init__(self, name: str, version: str, description: str = None):
        self.__name = name
        self.__description = description
        self.__version = version
        self.__dependencies = []
        self.__services = {}

    # Getter Methods

    def getName(self) -> str:
        return self.__name

    def getDescription(self) -> str:
        return self.__description

    def getVersion(self) -> str:
        return self.__version

    def getDependencies(self) -> list:
        return self.__dependencies

    def findAllServicePropertiesByInit(self, init: bool = False) -> dict:
        services = {}
        for id, serviceProps in self.__services.items():
            if serviceProps.getInit() == init:
                services[id] = serviceProps
        return services

    def getServicePropertiesById(self, sid: str) -> ServiceProperties:
        return self.__services.get(sid)

    # Setter Methods

    def setServiceProperties(self, services: list):
        for props in services:
            ModuleUtil.validateServiceProperties(self.__name, props)
            id = props.get('id')
            service = ServiceProperties(id, props.get('class'), props.get('args'))
            service.setInit(props.get('init'))
            service.setPath(props.get('path'))
            service.setModuleName(self.__name)
            self.__services[id] = service

    def setDependencies(self, dependencies: list):
        for depStr in dependencies:
            dependency = ModuleDependency(depStr)
            self.__dependencies.append(dependency)
