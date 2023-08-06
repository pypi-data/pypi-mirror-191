from ..config.AppConfigs import AppConfigs
from ..error.CmdExecError import CmdExecError
from ..module.AppModule import AppModule
from ..service.ArgumentService import ArgumentService
from ..service.ConfigurationService import ConfigurationService
from ..service.ServiceBuilder import ServiceBuilder


class AppContext:
    __configs: AppConfigs
    __services: dict
    __modules: dict

    def __init__(self):
        self.__configs = AppConfigs()
        self.__services = {}
        self.__modules = {}

    def __initCoreServices(self):
        configService = ConfigurationService(self.__configs)
        self.__services['configService'] = configService
        self.__services['argService'] = ArgumentService(configService)

    # Getter Methods

    def getConfig(self, key: str) -> object:
        return self.__configs.getValue(key)

    def getService(self, sid: str):
        if not self.hasService(sid):
            serviceProperties = ServiceBuilder.getServiceProperties(sid, self)
            service = ServiceBuilder.buildService(serviceProperties, self)
            self.addService(sid, service)
        return self.__services.get(sid)

    def getModules(self) -> list:
        return list(self.__modules.values())

    def getModule(self, name: str) -> AppModule:
        return self.__modules.get(name)

    def getConfigs(self) -> AppConfigs:
        return self.__configs

    def hasModule(self, name: str):
        module = self.__modules.get(name)
        return module is not None

    def hasService(self, sid: str):
        service = self.__services.get(sid)
        return service is not None

    def getInstancesByStr(self, ids: list) -> list:
        retList = []
        if ids is not None:
            for id in ids:
                if id == 'appConfigs':
                    retList.append(self.__configs)
                elif id.startswith('@'):
                    sid = id[1:]
                    service = self.getService(sid)
                    retList.append(service)
                else:
                    retList.append(id)
        return retList

    # Setter Methods

    def addModule(self, module: AppModule):
        name = module.getName()
        self.__modules[name] = module

    def addConfig(self, configs: dict):
        if configs is not None:
            self.__configs.addConfig(configs)

    def addService(self, sid: str, service: object):
        # Import class locally
        from ..service.AppService import AppService
        if service is None:
            raise CmdExecError('ERR26', {'sid': sid})
        elif not isinstance(service, AppService):
            raise CmdExecError('ERR28', {'cls': service.__class__.__name__})
        self.__services[sid] = service

    def printConfigs(self):
        self.__configs.print()

    # Utility Methods

    # def initService(self, serviceProps: ServiceProperties) -> object:
    #     from ..src.context.AppContextManager import AppContextManager
    #     from ..src.service.AppService import AppService
    #     if serviceProps is None:
    #         raise CmdExecError('ERR27')
    #     # Init service and return
    #     args = serviceProps.getArgs()
    #     passedArgs = []
    #     for arg in args:
    #         if arg['type'] == 'service':
    #             sid = arg['value']
    #             if self.hasService(sid):
    #                 service = self.getService(sid)
    #                 self.addService(sid, service)
    #             else:
    #                 props = self.getServiceProperties(sid)
    #                 service = self.initService(props)
    #                 self.addService(sid, service)
    #             passedArgs.append(service)
    #         elif arg['type'] == 'configs':
    #             passedArgs.append(self.__configs)
    #         else:
    #             passedArgs.append(arg['value'])
    #     clsPath = serviceProps.getClassPath()
    #     clsName = serviceProps.getClassName()
    #     ValidationUtil.failIfClassFileDoesNotExist(clsPath, 'ERR30', {'cls': clsName, 'path': clsPath})
    #     cls = ObjUtil.getClassFromClsPath(clsPath, clsName)
    #     if not issubclass(cls, AppService):
    #         raise CmdExecError('ERR28', {'src': clsName})
    #     service = ObjUtil.initClassFromStr(clsPath, clsName, passedArgs)
    #     contextManager = AppContextManager(self)
    #     service.setContextManager(contextManager)
    #     return service
