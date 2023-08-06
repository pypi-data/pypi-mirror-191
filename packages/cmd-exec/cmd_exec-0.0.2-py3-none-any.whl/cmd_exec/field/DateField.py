from ..error.CmdExecError import CmdExecError
from ..classes.FieldType import FieldType
from ..field.Field import Field
from ..util.DateUtil import DateUtil
from ..util.ValidationUtil import ValidationUtil


class DateField(Field):
    _format: str

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.DATE)
        self._format = '%m-%d-%Y'

    def setValue(self, value: object):
        try:
            if value is not None:
                ValidationUtil.failIfNotType(value, str, 'ERR55', {'fid': self._id, 'prop': 'value'})
                date = DateUtil.convertStrToDate(value, self._format)
                self._value = date
            else:
                self._value = self._default
        except Exception:
            raise CmdExecError('ERR55', {'fid': self._id, 'prop': 'value'})

    def setProperties(self, props: dict):
        super().setProperties(props)
        self._setFormat(props)
        self._setMin(props)
        self._setMax(props)

    def _setDefault(self, props: dict):
        try:
            dateStr = props.get('default')
            if dateStr is not None:
                ValidationUtil.failIfNotType(dateStr, str, 'ERR55', {'fid': self._id, 'prop': 'default'})
                date = DateUtil.convertStrToDate(dateStr, self._format)
                self._default = date
            else:
                self._default = None
        except Exception as exception:
            raise CmdExecError('ERR55',  {'fid': self._id, 'prop': 'default'})

    def _setFormat(self, props: dict):
        dateFormat = props.get('format')
        if dateFormat is not None:
            ValidationUtil.failIfNotType(dateFormat, str, 'ERR55', {'fid': self._id, 'prop': 'format'})
            self._format = dateFormat
        else:
            self._format = '%m-%d-%Y'

    def _setMin(self, props: dict):
        try:
            dateStr = props.get('min')
            if dateStr is not None:
                ValidationUtil.failIfNotType(dateStr, str, 'ERR55', {'fid': self._id, 'prop': 'min'})
                date = DateUtil.convertStrToDate(dateStr, self._format)
                self._min = date
            else:
                self.min = None
        except Exception as exception:
            raise CmdExecError('ERR55',  {'fid': self._id, 'prop': 'min'})

    def _setMax(self, props: dict):
        try:
            dateStr = props.get('max')
            if dateStr is not None:
                ValidationUtil.failIfNotType(dateStr, str, 'ERR55', {'fid': self._id, 'prop': 'max'})
                date = DateUtil.convertStrToDate(dateStr, self._format)
                self._max = date
            else:
                self.max = None
        except Exception as exception:
            raise CmdExecError('ERR55',  {'fid': self._id, 'prop': 'max'})

    def getFormat(self) -> str:
        return self._format

    def validate(self):
        super().validate()
        if self._value is None:
            pass
        elif self._min is not None and self._max is not None:
            if self._min.getValue() > self._value.getValue() or self._max.getValue() < self._value.getValue():
                raise CmdExecError('ERR56', {
                    'fid': self._id,
                    'value': self._value.toString(),
                    'from': self._min.toString(),
                    'to': self._max.toString()
                })
        elif self._min is not None and self._min.getValue() > self._value.getValue():
            raise CmdExecError('ERR56', {
                'fid': self._id,
                'value': self._value.toString(),
                'from': self._min.toString(),
                'to': '-'
            })
        elif self._max is not None and self._max.getValue() < self._value.getValue():
            raise CmdExecError('ERR56', {
                'fid': self._id,
                'value': self._value.toString(),
                'from': '-',
                'to': self._max.toString()
            })

    def print(self):
        print("====================================== Date Field =========================================")
        print("--- Common Properties ---")
        super().print()
        print("--- Date Field Properties ---")
        print('format: ' + str(self._format))
        if self._default is not None:
            print('default: ' + self._default.toString())
        if self._min is not None:
            print('min: ' + self._min.toString())
        if self._max is not None:
            print('max: ' + self._max.toString())
        if self._value is not None:
            print('value: ' + self._value.toString())
