from ..action import CmdActionResponse
from ..context.AppContextManager import AppContextManager
from ..menu.Command import Command


class CmdAction:
    _context: AppContextManager

    def setContextManager(self, contextManager: AppContextManager):
        self._context = contextManager

    def run(self, cmd: Command) -> CmdActionResponse:
        pass
