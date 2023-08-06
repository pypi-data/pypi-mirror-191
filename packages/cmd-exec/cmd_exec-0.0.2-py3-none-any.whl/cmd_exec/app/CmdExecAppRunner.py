import os
import sys
from ..app.CmdExecApp import CmdExecApp
from ..builder.AppContextBuilder import AppContextBuilder
from ..context.AppContext import AppContext
from ..context.AppContextManager import AppContextManager
from ..error.CmdExecError import CmdExecError
from ..service.ArgumentService import ArgumentService
from ..service.ConfigurationService import ConfigurationService
from ..util.ErrorUtil import ErrorUtil
from ..util.FileUtil import FileUtil
from ..util.ObjUtil import ObjUtil
from ..util.ValidationUtil import ValidationUtil


class CmdExecAppRunner:
    __isInitialized: bool = False
    __rootPath: str = None

    @staticmethod
    def initialize(env: str = 'production'):
        if not CmdExecAppRunner.__isInitialized:
            CmdExecAppRunner.__setRootDir(env)
            FileUtil.setRootPath(CmdExecAppRunner.__rootPath)
            CmdExecAppRunner.__isInitialized = True

    @staticmethod
    def run():
        try:
            CmdExecAppRunner.initialize()
            sys.path.append(CmdExecAppRunner.__rootPath)
            appContext = AppContextBuilder.buildBaseAppContext()
            app: CmdExecApp = CmdExecAppRunner.__buildCmdExecApp(appContext)
            app.run()
        except Exception as exp:
            ErrorUtil.handleException(exp)

    @staticmethod
    def __setRootDir(env: str):
        if CmdExecAppRunner.__rootPath is None:
            rootPath = os.environ['APP_RUNNER_ROOT_PATH']
            if env == 'test':
                rootPath = os.path.sep.join([rootPath, 'tests', 'target'])
            CmdExecAppRunner.__rootPath = rootPath

    @staticmethod
    def __buildCmdExecApp(appContext: AppContext) -> CmdExecApp:
        # Get Services
        argService: ArgumentService = appContext.getService('argService')
        configService: ConfigurationService = appContext.getService('configService')
        # Init CmdExeApp object
        mid = argService.getMode()
        props = configService.getModePropsById(mid)
        module = props.get('module')
        clsName = props.get('runner')
        if module is None:
            clsPath = '.app.{runner}'.format(**props)
        else:
            clsPath = 'modules.{module}.src.app.{runner}'.format(**props)
            # Validate
            ValidationUtil.failIfClassFileDoesNotExist(clsPath, 'ERR31', {'cls': clsName, 'path': clsPath})
        cls = ObjUtil.getClassFromClsPath(clsPath, clsName, 'cmd_exec')
        if not issubclass(cls, CmdExecApp):
            raise CmdExecError('ERR32', {'src': clsName, 'parent': 'CmdExecApp', 'name': props.get('module')})
        contextManager: AppContextManager = AppContextManager(appContext)
        app = ObjUtil.initClassFromStr(clsPath, clsName, [contextManager], 'cmd_exec')
        return app
