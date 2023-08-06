from ..context.AppContextManager import AppContextManager
from ..error.CmdExecError import CmdExecError
from ..module.ServiceProperties import ServiceProperties
from ..service.AppService import AppService
from ..service.ArgumentService import ArgumentService
from ..service.CommandService import CommandService
from ..service.ConfigurationService import ConfigurationService
from ..service.DatabaseService import DatabaseService
from ..service.ServiceType import ServiceType
from ..service.FieldService import FieldService
from ..service.LogService import LogService
from ..util.ObjUtil import ObjUtil
from ..util.StrUtil import StrUtil
from ..util.ValidationUtil import ValidationUtil


class ServiceBuilder:

    @staticmethod
    def buildService(serviceProps: ServiceProperties, appContext):
        if serviceProps is None:
            raise CmdExecError('ERR27')
        # Init service and return
        args = serviceProps.getArgs()
        passedArgs = []
        for arg in args:
            if arg['type'] == 'service':
                sid = arg['value']
                if appContext.hasService(sid):
                    service = appContext.getService(sid)
                else:
                    props = ServiceBuilder.getServiceProperties(sid, appContext)
                    service = ServiceBuilder.buildService(props, appContext)
                    appContext.addService(sid, service)
                passedArgs.append(service)
            elif arg['type'] == 'configs':
                configs = appContext.getConfigs()
                passedArgs.append(configs)
            else:
                passedArgs.append(arg['value'])
        clsPath = serviceProps.getClassPath()
        clsName = serviceProps.getClassName()
        ValidationUtil.failIfClassFileDoesNotExist(clsPath, 'ERR30', {'cls': clsName, 'path': clsPath})
        cls = ObjUtil.getClassFromClsPath(clsPath, clsName)
        if not issubclass(cls, AppService):
            raise CmdExecError('ERR28', {'src': clsName})
        service = ObjUtil.initClassFromStr(clsPath, clsName, passedArgs)
        contextManager = AppContextManager(appContext)
        service.setContextManager(contextManager)
        return service

    @staticmethod
    def getServiceProperties(sid, appContext) -> ServiceProperties:
        values = StrUtil.getModuleServiceMapFromStr(sid)
        mid = values.get('mid')
        if mid is not None:
            sid = values.get('sid')
            module = appContext.getModule(mid)
            return module.getServicePropertiesById(sid)
        else:
            for module in appContext.getModules():
                props = module.getServicePropertiesById(sid)
                if props is not None:
                    return props
        return None

    @staticmethod
    def buildConfigService(appContext) -> ConfigurationService:
        context = AppContextManager(appContext)
        configs = appContext.getConfigs()
        service = ConfigurationService(configs)
        service.setContextManager(context)
        return service

    @staticmethod
    def buildArgService(appContext) -> ArgumentService:
        context = AppContextManager(appContext)
        confService = appContext.getService(ServiceType.CONF_SERVICE)
        service = ArgumentService(confService)
        service.setContextManager(context)
        return service

    @staticmethod
    def buildCommandService(appContext) -> CommandService:
        context = AppContextManager(appContext)
        fieldService = appContext.getService(ServiceType.FIELD_SERVICE)
        argService = appContext.getService(ServiceType.ARG_SERVICE)
        service = CommandService(fieldService, argService)
        service.setContextManager(context)
        return service

    @staticmethod
    def buildFieldService(appContext) -> FieldService:
        context = AppContextManager(appContext)
        configService = appContext.getService(ServiceType.CONF_SERVICE)
        argService = appContext.getService(ServiceType.ARG_SERVICE)
        service = FieldService(configService, argService)
        service.setContextManager(context)
        return service

    @staticmethod
    def buildLogService(appContext) -> LogService:
        context = AppContextManager(appContext)
        confService = appContext.getService(ServiceType.CONF_SERVICE)
        service = LogService(confService)
        service.setContextManager(context)
        return service

    @staticmethod
    def buildDatabaseService(appContext) -> DatabaseService:
        # Fetch Configuration Service
        configService: ConfigurationService = appContext.getService('configService')
        # Fetch Database Settings
        settings = configService.getValue('database')
        service: DatabaseService = DatabaseService(settings)
        context = AppContextManager(appContext)
        service.setContextManager(context)
        service.initializeDatabase()
        return service
