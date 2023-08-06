
class MarkupBuilder:
    __text: str

    def __init__(self):
        self.__text = ""

    def setTextColorToRed(self):
        self.__text += '[red]'

    def resetTextColor(self):
        self.__text += '[rst]'

    def nextLine(self):
        self.__text += '[br]'

    def addConstraintText(self, text: str, size: int, align: str = 'left'):
        self.__text += "[txt:{size}:{align}:{text}]".format(size=size, align=align, text=text)

    def addDivider(self, length: int, lineChar: str = '-'):
        self.__text += "[rpt:{length}:{lineChar}]".format(length=length, lineChar=lineChar) + '[br]'

    def addHorizontalTable(self, cols: list, rows: list, title: str = None):
        tblText: str = ''
        width: int = 0
        for col in cols:
            label = col.get('label')
            length = col.get('length')
            width += length
            tblText += "| [ylw][txt:{length}:left:{label}][rst]".format(length=length, label=label)
        tblText += '|[br]'
        for i in range(len(rows)):
            tblText += '| '
            values = rows[i]
            colIndex = 0
            for value in values:
                length = cols[colIndex].get('length')
                tblText += "[txt:{length}:left:{value}]".format(length=length, value=value) + '| '
                colIndex += 1
            tblText += '[br]'
        width += (len(cols) * 2) + 1
        # Add Title
        if title is not None:
            tblText = "[rpt:{length}:-]".format(length=width) + '[br]' + tblText
            tblText = "| [ylw][txt:{size}:left:{text}][rst] |".format(size=(width - 4), text=title) + '[br]' + tblText
        # Add Borders
        tblText = "[rpt:{length}:-]".format(length=width) + '[br]' + tblText
        tblText += "[rpt:{length}:-]".format(length=width) + '[br]'
        self.__text += tblText

    def addVerticalTable(self, values: list, labelWidth: int, valueWidth: int):
        tblText: str = ''
        for props in values:
            label: str = props.get('label')
            value: str = props.get('value')
            tblText += "[ylw][txt:{width}:left:{text}] :[rst] ".format(width=labelWidth, text=label)
            tblText += "[txt:{width}:left:{text}]".format(width=valueWidth, text=value) + '[br]'
        self.__text += tblText

    def getMarkupText(self) -> str:
        return self.__text
