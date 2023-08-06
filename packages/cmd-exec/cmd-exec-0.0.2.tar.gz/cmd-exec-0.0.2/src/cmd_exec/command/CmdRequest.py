from ..field.Field import Field
from ..service.TerminalService import TerminalService


class CmdRequest:
    fields: dict
    terminalService: TerminalService

    def __init__(self, fields: dict, service: TerminalService):
        self.fields = fields
        self.terminalService = service

    def getField(self, fid: str) -> Field:
        return self.fields[fid]
