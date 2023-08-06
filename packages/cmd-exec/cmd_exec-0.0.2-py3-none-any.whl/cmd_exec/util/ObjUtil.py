import importlib

class ObjUtil:

    @staticmethod
    def initClassFromStr(clsPath: str, clsName: str, args: list = None, package: str = None) -> object:
        module = importlib.import_module(clsPath, package)
        cls = getattr(module, clsName)
        if args is None:
            obj = cls()
        else:
            obj = cls(*args)
        return obj

    @staticmethod
    def getClassFromClsPath(clsPath: str, clsName: str, package: str = None):
        module = importlib.import_module(clsPath, package)
        cls = getattr(module, clsName)
        return cls
