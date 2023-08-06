from html.parser import HTMLParser

from ..classes.HtmlElement import HtmlElement


class WebHtmlParser(HTMLParser):
    __rootElement: HtmlElement
    __currentElement: HtmlElement

    def __init__(self):
        super().__init__()
        self.__rootElement = None
        self.__currentElement = None

    def handle_starttag(self, tag, attrs):
        element = HtmlElement(tag, attrs, self.__currentElement)
        if self.__rootElement is None:
            self.__rootElement = element
            self.__currentElement = element
        else:
            self.__currentElement.addChild(element)
            self.__currentElement = element

    def handle_endtag(self, tag):
        self.__currentElement = self.__currentElement.getParent()

    def handle_data(self, data):
        self.__currentElement.addData(data)

    def getRootElement(self) -> HtmlElement:
        return self.__rootElement

    def parseStr(self, html: str):
        self.feed(html)

    def parseFile(self, filePath: str):
        file = open(filePath, 'r')
        content = file.read()
        self.parseStr(content)
