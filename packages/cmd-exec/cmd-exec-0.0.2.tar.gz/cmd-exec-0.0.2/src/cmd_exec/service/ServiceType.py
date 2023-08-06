
class ServiceType:
    ARG_SERVICE: str = 'argService'
    CMD_SERVICE: str = 'cmdService'
    CONF_SERVICE: str = 'configService'
    FIELD_SERVICE: str = 'fieldService'
    LOG_SERVICE: str = 'logService'
    TERMINAL_SERVICE: str = 'terminalService'

    __SERVICES: list = [
        ARG_SERVICE,
        CMD_SERVICE,
        CONF_SERVICE,
        FIELD_SERVICE,
        LOG_SERVICE
    ]

    @staticmethod
    def isCoreService( sid: str) -> bool:
        return sid in ServiceType.__SERVICES

    @staticmethod
    def isArgService(sid: str) -> bool:
        return sid == ServiceType.ARG_SERVICE

    @staticmethod
    def isCmdService(sid: str) -> bool:
        return sid == ServiceType.CMD_SERVICE

    @staticmethod
    def isConfService(sid: str) -> bool:
        return sid == ServiceType.CONF_SERVICE

    @staticmethod
    def isFieldService(sid: str) -> bool:
        return sid == ServiceType.FIELD_SERVICE

    @staticmethod
    def isLogService(sid: str) -> bool:
        return sid == ServiceType.LOG_SERVICE
