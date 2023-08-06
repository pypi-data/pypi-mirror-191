from ..config.AppConfigs import AppConfigs
from ..error.CmdExecError import CmdExecError
from ..log.LogSettings import LogSettings
from ..service.AppService import AppService


class ConfigurationService(AppService):
    __configs: AppConfigs

    def __init__(self, configs: AppConfigs):
        self.__configs = configs

    def getModeIds(self) -> list:
        modes = self.__configs.getValue('application.modes')
        if modes is None:
            return None
        elif not isinstance(modes, list):
            raise CmdExecError('ERR44')
        retList = []
        for props in modes:
            retList.append(props.get('id'))
        return retList

    def getDefaultMode(self) -> str:
        mode = self.__configs.getValue('application.default_mode')
        if mode is None:
            return None
        elif not isinstance(mode, str):
            raise CmdExecError('ERR42')
        return str(mode)

    def getModePropsById(self, mid: str) -> dict:
        modes = self.__configs.getValue('application.modes')
        retProps = None
        for props in modes:
            modId = props.get('id')
            if modId == mid:
                retProps = props
                break
        if retProps is not None:
            retProps['module'] = retProps.get('module')
        return retProps

    def getLogSettings(self) -> LogSettings:
        settings = self.__configs.getValue('log_settings')
        return LogSettings(settings)

    def getFieldClassProps(self, type: str) -> dict:
        fields = self.__configs.getValue('application.fields')
        for fieldProps in fields:
            ftype = fieldProps.get('type')
            if ftype == type:
                return fieldProps
        return None

    def getValue(self, path: str) -> object:
        return self.__configs.getValue(path)

    def isDatabaseSet(self):
        value: str = self.__configs.getValue('database.name')
        return value is not None
