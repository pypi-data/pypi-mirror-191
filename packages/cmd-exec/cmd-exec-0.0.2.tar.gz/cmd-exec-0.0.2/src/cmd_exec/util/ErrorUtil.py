import traceback

from ..error.CmdExecError import CmdExecError


class ErrorUtil:
    @staticmethod
    def handleException(exception: Exception):
        print('Error occurred while running application.')
        if isinstance(exception, CmdExecError):
            print('\nError Details(' + exception.getCode() + '):\n' + str(exception))
        else:
            print('\nError Details:\n' + str(exception))
        errorDetails: str = traceback.format_exc()
        print('\nStack Trace:\n ' + str(errorDetails))
