import os
from ..error.CmdExecError import CmdExecError
from ..util.FileUtil import FileUtil
from ..util.ListUtil import ListUtil
from ..util.StrUtil import StrUtil
from ..util.ValidationUtil import ValidationUtil


class ModuleUtil:

    @staticmethod
    def getModuleNames() -> list:
        modulesDirPath = FileUtil.getAbsolutePath(['modules'])
        directories = os.listdir(modulesDirPath, )
        ListUtil.deleteElements(directories, ['__pycache__'])
        return directories

    @staticmethod
    def validateModuleDirectoryAndFiles(name: str):
        path = ['modules']
        modulesPath = FileUtil.getAbsolutePath(path)
        # Validate Root Directory
        path.append(name)
        ValidationUtil.failIfDirectoryCanNotBeAccessed(path, 'ERR19', {'name': name, 'path': modulesPath})
        # Validate Settings File
        path.append(name + '.settings.yaml')
        settingsFilePath = FileUtil.getAbsolutePath(path)
        ValidationUtil.failIfFileCanNotBeAccessed(path, 'ERR06',  {'name': name, 'path': settingsFilePath})

    @staticmethod
    def validateModuleProperties(moduleName: str, props: dict):
        # Validate name property
        nameProp = props.get('name')
        ValidationUtil.failIfStrNoneOrEmpty(nameProp, 'ERR01', {'module': moduleName})
        if moduleName != nameProp:
            raise CmdExecError('ERR20', {'name': nameProp})
        # Validate version
        version = props.get('version')
        if StrUtil.isVersionSyntaxInvalid(version):
            raise CmdExecError('ERR02', {'version': version, 'module': moduleName})
        # Validate dependencies
        dependencies = props.get('dependencies')
        if dependencies is not None and not isinstance(dependencies, list):
            raise CmdExecError('ERR03', {'module': moduleName})
        # Validate Services
        services = props.get('services')
        if services is not None and not isinstance(services, list):
            raise CmdExecError('ERR24', {'name': moduleName})

    @staticmethod
    def validateServiceProperties(name: str, props: dict):
        # Validate id
        value = props.get('id')
        ValidationUtil.failIfNotType(value, str, 'ERR23', {'type': 'id', 'name': name})
        ValidationUtil.failIfStrNoneOrEmpty(value, 'ERR23', {'type': 'id', 'name': name})
        # Validate class
        cls = props.get('class')
        if cls is not None:
            ValidationUtil.failIfNotType(cls, str, 'ERR23', {'type': 'class', 'name': name})
        # Validate path
        path = props.get('path')
        if path is not None:
            ValidationUtil.failIfNotType(path, str, 'ERR23', {'type': 'path', 'name': name})
        ValidationUtil.failIfBothStrNoneOrEmpty([cls, path], 'ERR23', {'type': 'class or path', 'name': name})
        # Validate init
        init = props.get('init')
        if init is not None:
            ValidationUtil.failIfNotType(init, bool, 'ERR29', {'val': str(init), 'name': name})

    @staticmethod
    def validateModuleConfigs(name: str, configs: dict):
        for key, value in configs.items():
            ValidationUtil.failIfStringContainsChars(key, ['.'], 'ERR18', {'key': key, 'name': name})
            if isinstance(value, dict):
                ModuleUtil.validateModuleConfigs(name, value)

    @staticmethod
    def getModuleSettings(name: str) -> dict:
        settingsFileName = name + '.settings.yaml'
        return FileUtil.generateObjFromYamlFile(['modules', name, settingsFileName])

    @staticmethod
    def getModuleConfigs(name: str) -> dict:
        configFileName = name + '.config.yaml'
        path = ['modules', name, configFileName]
        ValidationUtil.failIfFileCanNotBeAccessed(path, 'ERR05', {'file': configFileName, 'name': name})
        return FileUtil.generateObjFromYamlFile(['modules', name, configFileName])

    @staticmethod
    def getModuleCommandProps(cid: str) -> dict:
        if StrUtil.isNoneOrEmpty(cid):
            raise CmdExecError('ERR60')
        props = StrUtil.getCommandPropertiesFromStr(cid)
        module = props.get('module')
        fileName = props.get('cid') + '.yaml'
        path = ['modules', module, 'commands', fileName]
        if module is not None and FileUtil.isFileReadable(path):
            return FileUtil.generateObjFromYamlFile(path)
        path = ['resources', 'commands', fileName]
        if FileUtil.isFileReadable(path):
            return FileUtil.generateObjFromYamlFile(path)
        raise CmdExecError('ERR34', {'file': fileName})

    @staticmethod
    def doesConfigFileExistForModule(name: str) -> bool:
        configFileName = name + '.config.yaml'
        path = ['modules', name, configFileName]
        return FileUtil.doesFileExist(path)
