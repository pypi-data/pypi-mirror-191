import getpass
import os
import platform


class SystemUtil:
    __SYSTEM_NAMES_WINDOWS: set = ['Windows']

    @staticmethod
    def isWindows() -> bool:
        osName: str = platform.system()
        return osName in SystemUtil.__SYSTEM_NAMES_WINDOWS

    @staticmethod
    def getCurrentUserName() -> str:
        username = getpass.getuser()
        return username

    @staticmethod
    def getCurrentUserGroups() -> list:
        if not SystemUtil.isWindows():
            return os.getgroups()
