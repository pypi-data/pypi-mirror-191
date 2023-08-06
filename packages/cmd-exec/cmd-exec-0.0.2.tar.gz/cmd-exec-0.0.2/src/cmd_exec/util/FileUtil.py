import math
import os
import shutil
import yaml
from ..error.CmdExecError import CmdExecError


class FileUtil:
    __rootPath: str = None

    @staticmethod
    def setRootPath(path: str):
        if not FileUtil.__rootPath:
            FileUtil.__rootPath = path

    @staticmethod
    def getRootPath() -> str:
        return FileUtil.__rootPath

    @staticmethod
    def getAbsolutePath(relativePath: list) -> str:
        return FileUtil.__rootPath + os.path.sep + os.path.sep.join(relativePath)

    @staticmethod
    def generateObjFromYamlFile(relativePath: list) -> dict:
        path = FileUtil.getAbsolutePath(relativePath)
        try:
            stream = open(path, 'r')
            retObj = yaml.load(stream, Loader=yaml.SafeLoader)
            if not isinstance(retObj, dict):
                raise CmdExecError('ERR22', {'path': path})
            return retObj
        except Exception as exp:
            msg = "Error occurred while parsing yaml file '{path}'.".format(path=path)
            raise CmdExecError(msg)

    @staticmethod
    def listFiles(relativePath: list) -> list:
        path = FileUtil.getAbsolutePath(relativePath)
        return os.listdir(path)

    # Query Methods

    @staticmethod
    def fileSize(path: str, blockSize: str) -> int:
        fileStats = os.stat(path)
        if blockSize == 'MB':
            return math.floor(fileStats.st_size / (1024 * 1024))
        elif blockSize == 'KB':
            return math.floor(fileStats.st_size/1024)
        return fileStats.st_size

    @staticmethod
    def isDirectoryReadable(relativePath: list):
        return FileUtil.isDirectory(relativePath) and FileUtil.doesDirectoryExist(relativePath) and FileUtil.doesUserHaveAccessOnFile(relativePath)

    @staticmethod
    def isFileReadable(relativePath: list):
        return not FileUtil.isDirectory(relativePath) and FileUtil.doesFileExist(relativePath) and FileUtil.doesUserHaveAccessOnFile(relativePath)

    @staticmethod
    def isDirectory(relativePath: list) -> bool:
        path = FileUtil.getAbsolutePath(relativePath)
        return os.path.isdir(path)

    @staticmethod
    def doesFileExist(relativePath: list, extension: str = '') -> bool:
        path = FileUtil.getAbsolutePath(relativePath)
        if extension != '':
            path = path + '.' + extension
        return os.path.exists(path)

    @staticmethod
    def doesDirectoryExist(relativePath: list) -> bool:
        path = FileUtil.getAbsolutePath(relativePath)
        return os.path.exists(path)

    @staticmethod
    def doesUserHaveAccessOnFile(relativePath: list) -> bool:
        path = FileUtil.getAbsolutePath(relativePath)
        return os.access(path, os.R_OK)

    # Directory or File Updating Commands

    @staticmethod
    def copyFile(srcPath: list, destPath: list):
        srcDirPath = FileUtil.getAbsolutePath(srcPath)
        destDirPath = FileUtil.getAbsolutePath(destPath)
        shutil.copy(srcDirPath, destDirPath)

    @staticmethod
    def copyDirectory(srcPath: list, destPath: list):
        srcDirPath = FileUtil.getAbsolutePath(srcPath)
        destDirPath = FileUtil.getAbsolutePath(destPath)
        shutil.copytree(srcDirPath, destDirPath)

    @staticmethod
    def makeDir(relativePath: list):
        if not FileUtil.doesFileExist(relativePath):
            path = FileUtil.getAbsolutePath(relativePath)
            os.mkdir(path)

    @staticmethod
    def deleteDir(relativePath: list, extraIgnoredDirs: list = ['modules']):
        ignoredDirs = ['src', 'logs', 'temp', 'app_runner'] + extraIgnoredDirs
        dirName = relativePath[-1]
        if dirName in ignoredDirs:
            raise CmdExecError('ERR21', {'dirs': str(ignoredDirs), 'home': FileUtil.__rootPath})
        if relativePath != [] and FileUtil.isDirectory(relativePath) and FileUtil.doesFileExist(relativePath) and dirName not in ignoredDirs:
            srcPath = FileUtil.getAbsolutePath(relativePath)
            shutil.rmtree(srcPath)

    @staticmethod
    def writeToFile(relativePath: list, content: str):
        path = FileUtil.getAbsolutePath(relativePath)
        file = open(path, 'w')
        file.write(content)
        file.close()

    @staticmethod
    def fromStrPathToArr(path: str) -> list:
        return path.split(os.path.sep)

    @staticmethod
    def readFile(path: list) -> str:
        absPath = FileUtil.getAbsolutePath(path)
        if FileUtil.isFileReadable(path):
            file = open(absPath, 'r')
            content: str = file.read()
            return content
        raise CmdExecError('ERR76', {'path': absPath})
