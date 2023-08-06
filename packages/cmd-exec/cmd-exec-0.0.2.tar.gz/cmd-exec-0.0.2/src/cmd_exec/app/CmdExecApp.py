from ..context.AppContextManager import AppContextManager
from ..service.ArgumentService import ArgumentService
from ..service.LogService import LogService


class CmdExecApp:
    _context: AppContextManager
    _logger: LogService
    _args: ArgumentService

    def __init__(self, contextManager: AppContextManager):
        self._context = contextManager
        self._logger = contextManager.getService('logService')
        self._args = contextManager.getService('argService')

    def run(self):
        pass
