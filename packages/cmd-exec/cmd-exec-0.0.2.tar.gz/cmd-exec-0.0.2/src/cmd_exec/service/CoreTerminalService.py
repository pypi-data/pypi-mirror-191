import re
from ..util.StrUtil import StrUtil
from ..classes.TextColor import TextColor
from ..service.AppService import AppService


class CoreTerminalService(AppService):
    colorCodes: dict = {
        'red': TextColor.RED,
        'grn': TextColor.GREEN,
        'ylw': TextColor.YELLOW,
        'cyn': TextColor.CYAN,
        'rst': TextColor.RESET,
        'bld': TextColor.BOLD
    }

    def print(self, text: str, model: dict = {}):
        text = self.__removeNewLine(text)
        text = self.__importColorCodes(text)
        text = self.__parseBreakLineTag(text)
        text = self.__parseRowTag(text)
        text = self.__parseRepeatTag(text)
        text = self.__insertModelData(text, model)
        print(text)

    def __removeNewLine(self, text: str) -> str:
        return text.replace('\n', '[br]')

    def __insertModelData(self, text: str, model: dict) -> str:
        for key, value in model.items():
            replaceWith = '{{' + key + '}}'
            text = text.replace(replaceWith, value)
        return text

    def __importColorCodes(self, text: str) -> str:
        for id, code in self.colorCodes.items():
            text = text.replace("[" + id + "]", code)
        return text

    def __parseBreakLineTag(self, text: str) -> str:
        return text.replace('[br]', '\n')

    def __parseRowTag(self, text: str) -> str:
        pattern = '\[(txt):(\d+):(left|right|center):([^\\]]*)\]'
        m = re.search(pattern, text)
        while m is not None:
            results: tuple = m.groups()
            trgStr = m.group(0)
            replaceWith = StrUtil.getAlignedAndLimitedStr(results[3], int(results[1]), results[2])
            text = text.replace(trgStr, replaceWith)
            m = re.search(pattern, text)
        return text

    def __parseRepeatTag(self, text: str) -> str:
        pattern = '\[(rpt):(\d+):([^\\]]*)\]'
        m = re.search(pattern, text)
        while m is not None:
            results: tuple = m.groups()
            trgStr = m.group(0)
            replaceWith = results[2] * int(results[1])
            text = text.replace(trgStr, replaceWith)
            m = re.search(pattern, text)
        return text
