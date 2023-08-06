from ..classes.FieldType import FieldType
from ..error.CmdExecError import CmdExecError
from ..util.ValidationUtil import ValidationUtil


class Field:
    _id: str
    _type: str
    _label: str
    _required: bool
    _value: object
    _default: object
    _min: object
    _max: object

    def __init__(self, id: str, ftype: str):
        self._id = id
        self._type = ftype
        self._label = None
        self._required = False
        self._value = None
        self._default = None
        self._min = None
        self._max = None

    def setProperties(self, props: dict):
        # Set label field
        label = props.get('label')
        self.setLabel(label)
        # Set required field
        required = props.get('required')
        self._setRequired(required)
        self._setDefault(props)

    def setLabel(self, label: object):
        ValidationUtil.failIfNotType(label, str, 'ERR55', {'fid': self._id, 'prop': 'label'})
        self._label = str(label)

    def setValue(self, value: object):
        self._value = value

    def _setRequired(self, value: object):
        if value is not None:
            ValidationUtil.failIfNotType(value, bool, 'ERR55', {'fid': self._id, 'prop': 'required'})
            self._required = str(value) == 'True'

    def _setDefault(self, props: dict):
        pass

    def isRequired(self) -> bool:
        return self._required

    def isRequiredAndHaveNoValue(self) -> bool:
        return self.isRequired() and self._value is None

    def getId(self) -> str:
        return self._id

    def getValue(self) -> object:
        return self._value

    def getType(self) -> str:
        return self._type

    def getLabel(self) -> str:
        return self._label

    def isDate(self) -> bool:
        return self._type == FieldType.DATE

    def isSelection(self) -> bool:
        return self._type == FieldType.SELECTION

    def isText(self) -> bool:
        return self._type == FieldType.TEXT

    def validate(self):
        if self.isRequired() and self._value is None:
            raise CmdExecError('ERR57', {'fid': self._id})

    def print(self):
        print('id: ' + self._id + ' | type: ' + self._type + ' | label: ' + self._label + ' | required: ' + str(self._required))
