from json_jsx.JSONParser import JSONParser
from json_jsx.JSONListener import JSONListener


class JsxEmitter(JSONListener):
    def __init__(self):
        self.pairTags = []
        self.typeTags = []
        self.ts = {}

    def getJSX(self, elem):
        return self.ts[elem]

    def setJSX(self, elem, value):
        self.ts[elem] = value

    def exitAtom(self, elem):
        self.setJSX(elem, elem.getText())

    def exitString(self, elem):
        if "props" in self.pairTags:
            self.setJSX(elem, elem.getText())
        else:
            self.setJSX(elem, elem.getText().strip('"'))

    def exitObjectValue(self, elem: JSONParser.ObjectValueContext):
        self.setJSX(elem, self.getJSX(elem.obj()))

    def enterPair(self, elem: JSONParser.PairContext):
        tag = elem.STRING().getText().strip('"')
        self.pairTags.append(tag)

    def exitPair(self, elem: JSONParser.PairContext):
        tag = elem.STRING().getText().strip('"')
        val = self.getJSX(elem.value())
        if tag == "type":
            self.typeTags.append(val)
            x = '<%s' % val
        elif tag == "props":
            x = '%s>' % val
        elif (len(self.pairTags) >= 2) and self.pairTags[-2] == "props":
            x = '%s = {%s}\n' % (tag, val)
        elif tag == "children":
            x = "%s</%s>" % (val, self.typeTags.pop())
        else:
            x = '%s: %s,\n' % (tag, val)
        self.setJSX(elem, x)
        self.pairTags.pop()

    def exitAnObject(self, elem: JSONParser.AnObjectContext):
        buf = "\n"
        for pelem in elem.pair():
            buf += self.getJSX(pelem)
        if (len(self.pairTags) >= 2) and self.pairTags[-2] == "props":
            buf = '{%s}' % buf
        self.setJSX(elem, buf)

    def exitArrayOfValues(self, elem: JSONParser.ArrayOfValuesContext):
        buf = "\n"
        for velem in elem.value():
            buf += '%s\n' % self.getJSX(velem)
        self.setJSX(elem, buf)

    def exitArrayValue(self, elem: JSONParser.ArrayValueContext):
        self.setJSX(elem, self.getJSX(elem.array()))

    def exitEmptyArray(self, elem: JSONParser.EmptyArrayContext):
        self.setJSX(elem, "")

    def exitJson(self, elem: JSONParser.JsonContext):
        self.setJSX(elem, self.getJSX(elem.getChild(0)))
