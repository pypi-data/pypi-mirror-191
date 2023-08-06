import copy
import sqlite3
from ..error.CmdExecError import CmdExecError
from ..database.Column import Column
from ..database.DomainObject import DomainObject
from ..service.ConfigurationService import ConfigurationService
from ..util.FileUtil import FileUtil
from ..service.AppService import AppService


class DatabaseService(AppService):
    __configService: ConfigurationService
    __settings: dict
    __connection: object
    __dbName: str

    def __init__(self, settings: dict = {}):
        if settings is None:
            self.__settings = {}
        else:
            self.__settings = settings
        self.__setDatabaseName()
        self.__connection = None

    def initializeDatabase(self):
        self.__configService = self._contextManager.getService('configService')
        if not self.__doesDatabaseExist():
            self.connect()
            fileName: str = self.__configService.getValue('database.initialization.file')
            if fileName is not None:
                sql: str = self.__readSqlFile(fileName)
                cursor = self.__connection.cursor()
                cursor.execute(sql)
                self.__connection.commit()
            self.disconnect()

    def __readSqlFile(self, fileName: str) -> str:
        sqlFilePath: list = ['resources', 'databases', fileName]
        content: str = FileUtil.readFile(sqlFilePath)
        return content

    def __doesDatabaseExist(self) -> bool:
        path: list = ['resources', 'databases', self.__dbName]
        return FileUtil.isFileReadable(path)

    def __setDatabaseName(self):
        name = self.__settings.get('name')
        if name is None:
            self.__dbName = 'main.db'
        else:
            self.__dbName = name

    def connect(self):
        if self.__connection is None:
            path: str = FileUtil.getAbsolutePath(['resources', 'databases', self.__dbName])
            self.__connection = sqlite3.connect(path)

    def disconnect(self):
        self.__connection.close()
        self.__connection = None

    def list(self, obj: DomainObject) -> list:
        self.connect()
        table = obj.getTableName()
        columns = obj.getColumns()
        sql = 'SELECT * FROM ' + table
        self.__connection.row_factory = sqlite3.Row
        cursor = self.__connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        retList: list = []
        while row is not None:
            copiedObj = copy.deepcopy(obj)
            for column in columns:
                name = column.getTitle()
                value = row[name]
                copiedObj.addValue(name, value)
            retList.append(copiedObj)
            row = cursor.fetchone()
        self.disconnect()
        return retList

    def insert(self, obj: DomainObject):
        self.connect()
        table = obj.getTableName()
        columns = obj.getColumns()
        sql = "INSERT INTO " + table + ' ('
        for column in columns:
            sql += column.getTitle() + ','
        sql = sql[:-1]
        sql += ')'
        sql += ' VALUES ('
        for column in columns:
            name = column.getTitle()
            if column.isText():
                sql += "'" + obj.getValue(name) + "',"
            elif column.isNumber():
                sql += obj.getValue(name) + ","
        sql = sql[:-1]
        sql += ')'
        cursor = self.__connection.cursor()
        cursor.execute(sql)
        self.__connection.commit()
        self.disconnect()

    def delete(self, obj: DomainObject):
        self.connect()
        table = obj.getTableName()
        sql = "DELETE FROM " + table
        column: Column = obj.getPrimaryColumn()
        name = column.getTitle()
        value = obj.getValue(name)
        if column.isText():
            sql += " WHERE " + column.getTitle() + "='" + value + "'"
        elif column.isNumber():
            sql += " WHERE " + column.getTitle() + "=" + value
        else:
            raise CmdExecError('ERR77')
        cursor = self.__connection.cursor()
        cursor.execute(sql)
        self.__connection.commit()
        self.disconnect()

    def executeUpdateQuery(self, sql: str):
        self.connect()
        cursor = self.__connection.cursor()
        cursor.execute(sql)
        self.__connection.commit()
        self.disconnect()

    def executeSelectQuery(self, sql: str) -> list:
        self.connect()
        cursor = self.__connection.cursor()
        cursor.execute(sql)
        retList = cursor.fetchall()
        self.disconnect()
        return retList
