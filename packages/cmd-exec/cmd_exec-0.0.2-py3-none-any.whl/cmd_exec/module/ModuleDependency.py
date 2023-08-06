from ..error.CmdExecError import CmdExecError
from ..util.ListUtil import ListUtil
from ..util.StrUtil import StrUtil


class ModuleDependency:
    __name: str
    __operator: str
    __version: str

    def __init__(self, depStr: str):
        values = depStr.split('|')
        self.__name = ListUtil.getByIndex(values, 0)
        self.__operator = ListUtil.getByIndex(values, 1)
        self.__version = ListUtil.getByIndex(values, 2)
        self.__validateDependencyStr(depStr)

    # Getter Methods

    def getModuleName(self) -> str:
        return self.__name

    def hasNoVersion(self) -> bool:
        return self.__operator is None

    # Utility Methods

    def validate(self, dependingModName: str, trgVersion: str = None, doesTrgModVersionExist: bool = False):
        filledDepModVersion = StrUtil.prefillVersion(self.__version)
        filledTrgModVersion = StrUtil.prefillVersion(trgVersion)
        if self.hasNoVersion() and not doesTrgModVersionExist:
            raise CmdExecError('ERR07', {'srcModule': dependingModName, 'depModule': self.__name})
        elif self.__operator == '=' and filledDepModVersion != filledTrgModVersion:
            raise CmdExecError('ERR08', {'srcModule': dependingModName, 'depModule': self.__name, 'depVersion': self.__version, 'trgVersion': trgVersion})
        elif self.__operator == '>' and filledTrgModVersion <= filledDepModVersion:
            raise CmdExecError('ERR09', {'srcModule': dependingModName, 'depModule': self.__name, 'depVersion': self.__version, 'trgVersion': trgVersion})
        elif self.__operator == '<' and filledTrgModVersion >= filledDepModVersion:
            raise CmdExecError('ERR10', {'srcModule': dependingModName, 'depModule': self.__name, 'depVersion': self.__version, 'trgVersion': trgVersion})
        elif self.__operator == '<=' and filledTrgModVersion > filledDepModVersion:
            raise CmdExecError('ERR11', {'srcModule': dependingModName, 'depModule': self.__name, 'depVersion': self.__version, 'trgVersion': trgVersion})
        elif self.__operator == '>=' and filledTrgModVersion < filledDepModVersion:
            raise CmdExecError('ERR12', {'srcModule': dependingModName, 'depModule': self.__name, 'depVersion': self.__version, 'trgVersion': trgVersion})

    # Private Methods

    def __validateDependencyStr(self, depStr: str):
        if depStr is None:
            raise CmdExecError('ERR13')
        values = depStr.split('|')
        if len(values) == 1:
            return
        if len(values) == 2:
            raise CmdExecError("ERR14", {'id': depStr})
        elif len(values) > 3:
            raise CmdExecError("ERR15", {'id': depStr})
        elif values[1] not in ['=', '<', '>', '>=', '<=']:
            raise CmdExecError("ERR16", {'id': depStr})
        elif StrUtil.isVersionSyntaxInvalid(values[2]):
            raise CmdExecError('ERR17', {'depModule': values[0], 'version': values[2], 'module': self.__name})
