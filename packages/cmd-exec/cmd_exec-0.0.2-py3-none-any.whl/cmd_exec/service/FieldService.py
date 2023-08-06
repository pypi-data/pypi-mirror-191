from ..context.AppContextManager import AppContextManager
from ..error.CmdExecError import CmdExecError
from ..field.Field import Field
from ..field.OptionProvider import OptionProvider
from ..field.SelectionField import SelectionField
from ..menu.Command import Command
from ..service.AppService import AppService
from ..service.ArgumentService import ArgumentService
from ..service.ConfigurationService import ConfigurationService
from ..util.FileUtil import FileUtil
from ..util.ObjUtil import ObjUtil
from ..util.ValidationUtil import ValidationUtil


class FieldService(AppService):
    __configService: ConfigurationService
    __argService: ArgumentService

    def __init__(self, configService: ConfigurationService, argService: ArgumentService):
        self.__configService = configService
        self.__argService = argService

    def setContextManager(self, contextManager: AppContextManager):
        self._contextManager = contextManager

    def buildField(self, cmd: Command, props: dict) -> Field:
        cid = cmd.getId()
        self.__validateRequiredProps(cid, props)
        fieldType = props.get('type')
        fid = props.get('id')
        if fieldType is None:
            raise CmdExecError('ERR53', {'cid': cid, 'type': type})
        clsProps: dict = self.__getFieldClassProps(fieldType)
        cls = clsProps.get('class')
        clsPath = clsProps.get('path')
        field: Field = ObjUtil.initClassFromStr(clsPath, cls, [fid], 'cmd_exec')
        field.setProperties(props)
        if field.getType() == 'selection':
            self.__insertOptionsFromOptionProvider(cmd.getModule(), field, props)
        return field

    def __insertOptionsFromOptionProvider(self, module: str, field: SelectionField, props: dict):
        optionProviderProps = props.get('option_provider')
        if optionProviderProps is not None:
            fid = props.get('id')
            ValidationUtil.failIfNotType(optionProviderProps, dict, 'ERR55', {'fid': fid, 'prop': 'option_provider'})
            # Set Executor
            clsName = optionProviderProps.get('class')
            ValidationUtil.failIfStrNoneOrEmpty(clsName, 'ERR55', {'fid': fid, 'prop': 'option_provider > class'})
            clsPath = 'modules.{module}.src.provider.{cls}'.format(cls=clsName, module=module)
            ValidationUtil.failIfClassFileDoesNotExist(clsPath, 'ERR51', {'path': clsPath})
            cls = ObjUtil.getClassFromClsPath(clsPath, clsName)
            ValidationUtil.failIfNotSubClass(cls, OptionProvider)
            optionProvider: OptionProvider = ObjUtil.initClassFromStr(clsPath, clsName)
            optionProvider.setContextManager(self._contextManager)
            options = optionProvider.getOptions()
            field.appendOptions(options)

    def __getFieldClassProps(self, fieldType: str) -> dict:
        fieldClsProps = self.__configService.getFieldClassProps(fieldType)
        ValidationUtil.failIfNotType(fieldClsProps, dict, 'ERR50', {'type': type})
        cls = fieldClsProps.get('class')
        ValidationUtil.failIfStrNoneOrEmpty(cls, 'ERR47', {'type': type})
        mid = fieldClsProps.get('module')
        clsPath = fieldClsProps.get('path')
        if clsPath is not None:
            ValidationUtil.failIfNotType(clsPath, str, 'ERR48', {'type': 'string'})
            path = clsPath
        elif mid is not None:
            ValidationUtil.failIfNotType(mid, str, 'ERR48', {'type': 'module'})
            path = 'modules.{module}.src.field.{cls}'.format(module=mid, cls=cls)
        else:
            path = 'field.{cls}'.format(cls=cls)
        return {'class': cls, 'path': path}

    def __validateRequiredProps(self, cid: str, props: dict):
        type = props.get('type')
        ValidationUtil.failIfStrNoneOrEmpty(type, 'ERR54', {'cid': cid, 'property': 'type'})
        fid = props.get('id')
        ValidationUtil.failIfStrNoneOrEmpty(fid, 'ERR54', {'cid': cid, 'property': 'id'})
        label = props.get('label')
        ValidationUtil.failIfStrNoneOrEmpty(label, 'ERR54', {'cid': cid, 'property': 'label'})

    def getFieldValuesFromArgumentFile(self, cmd: Command) -> dict:
        argFileName = cmd.getId() + '.args.yaml'
        path = ['resources', 'arguments', argFileName]
        if FileUtil.doesFileExist(path):
            return FileUtil.generateObjFromYamlFile(path)
        return {}

    def getFieldValuesFromCmdArgs(self, cmd: Command) -> dict:
        args: dict = {}
        fieldIds: list = cmd.getFieldIds()
        passedArgs: dict = self.__argService.getArgs()
        for fid in fieldIds:
            args[fid] = passedArgs.get(fid)
        return args
