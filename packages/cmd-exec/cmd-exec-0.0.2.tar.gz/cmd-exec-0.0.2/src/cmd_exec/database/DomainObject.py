from ..database.Column import Column


class DomainObject:
    _primaryKey: str
    _properties: dict
    _columns: list
    _values: dict

    def __init__(self):
        self.setProperties()
        self.__setColumns()
        self._values = {}

    def setProperties(self):
        pass

    def __setColumns(self):
        columns = self._properties.get('columns')
        self._columns = []
        if columns is not None:
            for column in columns:
                isPrimary = column.get('is_primary_key')
                if isPrimary is None:
                    isPrimary = False
                col = Column(column.get('name'), column.get('type'), isPrimary)
                self._columns.append(col)

    def getTableName(self) -> str:
        return self._properties.get('table')

    def getColumns(self) -> list:
        return self._columns

    def getPrimaryColumn(self) -> Column:
        for column in self._columns:
            if column.isPrimary():
                return column
        return None

    def addValue(self, name: str, value: str):
        self._values[name] = value

    def getValue(self, name: str) -> str:
        return self._values.get(name)

    def toString(self) -> str:
        resp: str = ''
        for key, val in self._values.items():
            resp += key + ' : ' + val + ' | '
        return resp
