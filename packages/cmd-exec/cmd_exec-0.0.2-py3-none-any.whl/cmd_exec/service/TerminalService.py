from ..field.Field import Field
from ..service.AppService import AppService


class TerminalService(AppService):

    def print(self, text: str, model: dict = {}):
        pass

    def getFieldValue(self, field: Field):
        pass

    def getFieldValues(self, fields: list):
        pass
