from ..context.AppContextManager import AppContextManager


class OptionProvider:
    _contextManager: AppContextManager

    # Setter Methods

    def setContextManager(self, contextManager: AppContextManager):
        self._contextManager = contextManager

    def getOptions(self) -> list:
        pass
