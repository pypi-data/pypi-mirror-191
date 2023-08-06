

class AppContextManager:
    __appContext: object

    def __init__(self, appContext: object):
        self.__appContext = appContext

    # Getter Methods

    def getConfig(self, key: str):
        return self.__appContext.getConfig(key)

    def getService(self, sid: str):
        return self.__appContext.getService(sid)
