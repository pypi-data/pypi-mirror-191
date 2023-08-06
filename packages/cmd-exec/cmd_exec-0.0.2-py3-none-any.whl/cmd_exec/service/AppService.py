from ..context.AppContextManager import AppContextManager


class AppService:
    _contextManager: AppContextManager

    # Setter Methods

    def setContextManager(self, contextManager: AppContextManager):
        self._contextManager = contextManager
