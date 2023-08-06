from ..config.ConfigKey import ConfigKey
from ..config.ConfigValue import ConfigValue
from ..error.CmdExecError import CmdExecError


class ConfigManager:
    __configs: dict = None

    def __init__(self, configs: dict = {}):
        self.__configs = configs

    def save(self, configs: dict):
        if self.__configs is {}:
            self.__configs = configs
        else:
            self.__saveConfigs(self.__configs, configs)

    def __saveConfigs(self, destConfigs: dict, newConfigs: dict):
        for key, newVal in newConfigs.items():
            newConfKey = ConfigKey(key)
            val = destConfigs.get(newConfKey.getKey())
            currConfVal = ConfigValue(val)
            newConfVal = ConfigValue(newVal)

            if not newConfKey.isValidKey():
                raise CmdExecError('ERR63', {'key': newConfKey.getRawKey()})
            elif currConfVal.isNull():
                destConfigs[newConfKey.getKey()] = newConfVal.getValue()
                continue
            elif newConfVal.isDict() and currConfVal.isDict():
                self.__saveConfigs(currConfVal.getValue(), newConfVal.getValue())
            elif currConfVal.hasTypeMismatch(newConfVal):
                raise CmdExecError('ERR64', {'existingVal': currConfVal.getValueAsStr(), 'newVal': newConfVal.getValueAsStr()})
            elif newConfKey.isAddKey():
                currConfVal.appendValue(newConfVal)
                destConfigs[newConfKey.getKey()] = currConfVal.getValue()
            else:
                destConfigs[newConfKey.getKey()] = newConfVal.getValue()

    def getValue(self, keys: list) -> object:
        configs: dict = self.__configs
        count: int = len(keys)
        for i in range(count):
            key = keys[i]
            value = configs.get(key)
            if i == count - 1:
                return value
            elif isinstance(value, dict):
                configs = value
        return None

    def toString(self):
        return self.__toString(self.__configs, 0)

    def __toString(self, configs: dict, indent: int) -> str:
        indent += 1
        text: str = ''
        for key, value in configs.items():
            text += (' ' * indent) + key + ' : '
            if isinstance(value, dict):
                text += '\n' + self.__toString(value, indent)
            else:
                text += str(value) + '\n'
        return text
