import getpass

from ..command.CmdExecutor import CmdExecutor
from ..error.CmdExecError import CmdExecError


class Command:
    _id: str
    _title: str
    _executor: CmdExecutor
    _fields: dict
    _module: str
    _allowedUsers: list
    _deniedUsers: list
    _allowedGroups: list
    _deniedGroups: list

    def __init__(self, cid: str, title: str, module: str):
        self._id = cid
        self._title = title
        self._fields = {}
        self._executor = None
        self._module = module
        self._allowedUsers = None
        self._deniedUsers = None
        self._allowedGroups = None
        self._deniedGroups = None

    def setExecutor(self, executor: CmdExecutor):
        self._executor = executor

    def setAllowedUsers(self, users: list):
        self._allowedUsers = users

    def setDeniedUsers(self, users: list):
        self._deniedUsers = users

    def setAllowedGroups(self, groups: list):
        self._allowedGroups = groups

    def setDeniedGroups(self, groups: list):
        self._deniedGroups = groups

    def validateUserPermission(self, userName: str):
        cmdDesc: str = self._id + ' : ' + self._title
        if self._allowedUsers is not None:
            isDenied = userName not in self._allowedUsers
            if isDenied:
                raise CmdExecError('ERR78', {'user': userName, 'users': self._allowedUsers, 'cmd': cmdDesc})

        if self._deniedUsers is not None:
            isDenied = userName in self._deniedUsers
            if isDenied:
                raise CmdExecError('ERR79', {'user': userName, 'users': self._deniedUsers, 'cmd': cmdDesc})

    def validateUserGroupPermission(self, userName: str, groupNames: list):
        cmdDesc: str = self._id + ':' + self._title
        if self._allowedGroups is not None:
            matches: set = set(groupNames).intersection(self._allowedGroups)
            if len(matches) == 0:
                raise CmdExecError('ERR80', {'user': userName, 'groups': groupNames, 'cmd': cmdDesc})
        if self._deniedGroups is not None:
            matches: set = set(groupNames).intersection(self._deniedGroups)
            if len(matches) > 0:
                raise CmdExecError('ERR81', {'user': userName, 'groups': groupNames, 'cmd': cmdDesc})

    def setFields(self, fields: list):
        if fields is not None and isinstance(fields, list):
            for field in fields:
                self._fields[field.getId()] = field

    def setValues(self, values: dict):
        if values is not None and isinstance(values, dict):
            for fid, field in self._fields.items():
                value = values.get(fid)
                field.setValue(value)

    def getId(self) -> str:
        return self._id

    def getExecutor(self) -> CmdExecutor:
        return self._executor

    def getFields(self) -> dict:
        return self._fields

    def getFieldIds(self) -> list:
        return list(self._fields.keys())

    def getModule(self) -> str:
        return self._module

    def print(self):
        print('id: ' + self._id + ' | title: ' + self._title)
