from ..error.CmdExecError import CmdExecError
from ..classes.FieldType import FieldType
from ..field.Field import Field


class TextField(Field):
    _value: str

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.TEXT)

    def setValue(self, value: str):
        if value is None and self._default is not None:
            self._value = self._default
        else:
            self._value = value

    def setProperties(self, props: dict):
        super().setProperties(props)
        self.__setMinSize(props)
        self.__setMaxSize(props)

    def validate(self):
        super().validate()
        if self._min is not None and len(self._value) < self._min:
            raise CmdExecError('ERR61', {'value': self._value, 'fid': self.getId(), 'min_size': str(self._min)})
        if self._max is not None and len(self._value) > self._max:
            raise CmdExecError('ERR62', {'value': self._value, 'fid': self.getId(), 'max_size': str(self._max)})

    def _setDefault(self, props: dict):
        self._default = props.get('default')

    def __setMinSize(self, props: dict):
        value = props.get('min_size')
        if value is not None and not isinstance(value, int):
            raise CmdExecError('ERR55', {'fid': self.getId(), 'prop': 'min_size'})
        self._min = value

    def __setMaxSize(self, props: dict):
        value = props.get('max_size')
        if value is not None and not isinstance(value, int):
            raise CmdExecError('ERR55', {'fid': self.getId(), 'prop': 'max_size'})
        self._max = value

    def getValue(self) -> str:
        return self._value

    def print(self):
        print("====================================== Text Field =========================================")
        print("--- Common Properties ---")
        super().print()
        print("--- Text Field Properties ---")
        print('Value: ' + self._value)
