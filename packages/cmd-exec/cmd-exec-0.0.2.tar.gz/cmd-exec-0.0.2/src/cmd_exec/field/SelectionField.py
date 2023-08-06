from ..classes.Option import Option
from ..classes.FieldType import FieldType
from ..error.CmdExecError import CmdExecError
from ..field.Field import Field
from ..util.StrUtil import StrUtil
from ..util.ValidationUtil import ValidationUtil


class SelectionField(Field):
    _options: list
    _selectedOptions: list

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.SELECTION)
        self._options = []
        self._selectedOptions = []

    def appendOptions(self, options: list):
        self._options += options

    def setProperties(self, props: dict):
        super().setProperties(props)
        self.__setMin(props)
        self.__setMax(props)
        self.__setOptions(props)

    def __setOptions(self, props: dict):
        options: list = props.get('options')
        if options is not None:
            ValidationUtil.failIfNotType(options, list, 'ERR55', {'fid': self._id, 'prop': 'options'})
            for props in options:
                option = Option(props.get('id'), props.get('label'))
                self._options.append(option)

    def __setMin(self, props: dict):
        minVal = props.get('min')
        if minVal is not None:
            ValidationUtil.failIfNotType(minVal, int, 'ERR55', {'fid': self._id, 'prop': 'min'})
            self._min = minVal

    def __setMax(self, props: dict):
        maxVal = props.get('max')
        if maxVal is not None:
            ValidationUtil.failIfNotType(maxVal, int, 'ERR55', {'fid': self._id, 'prop': 'max'})
            self._max = maxVal

    def _setDefault(self, props: dict):
        defaultOptionIds = props.get('default')
        if defaultOptionIds is not None:
            ValidationUtil.failIfNotType(defaultOptionIds, list, 'ERR65', {'fid': self._id})
            self._default = defaultOptionIds

    def setValue(self, value: str):
        if StrUtil.isNoneOrEmpty(value) and self._default is not None:
            ids = self._default
        elif not StrUtil.isNoneOrEmpty(value):
            ids = value.split(',')
        else:
            ids = []
        self.__selectOptionsByIds(ids)

    def __selectOptionsByIds(self, ids: list):
        if ids is not None and len(ids) > 0:
            for option in self._options:
                if option.getId() in ids:
                    self._selectedOptions.append(option)

    def getSelectedOptions(self) -> list:
        return self._selectedOptions

    def getOptions(self) -> list:
        return self._options

    def validate(self):
        selectedOptionCount = len(self._selectedOptions)
        if self._min is not None and selectedOptionCount < self._min:
            raise CmdExecError('ERR67', {'fid': self._id, 'min': self._min})
        elif self._max is not None and selectedOptionCount > self._max:
            raise CmdExecError('ERR68', {'fid': self._id, 'max': self._max})

    def print(self):
        print("====================================== Selection Field =========================================")
        print("--- Common Properties ---")
        super().print()
        print("--- Selection Field Properties ---")
        print('options: ' + str(self._options))
