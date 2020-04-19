import re

from antlr4 import TerminalNode

from MAPYVisitor import MAPYVisitor
from MAPYParser import MAPYParser


class LaTeXEmitter(MAPYVisitor):

    latex: str
    level: int

    def __init__(self):
        self.latex = ("\\documentclass[12pt, a4paper]{article}\n"
                      "\n"
                      "\\usepackage[left = 1.5cm, right = 1.5cm, top = 1.5cm, bottom = 1.5cm]{geometry}\n"
                      "\n"
                      "\\usepackage{cmap}\n"
                      "\n"
                      "\\usepackage[T2A]{fontenc}\n"
                      "\\usepackage[utf8]{inputenc}\n"
                      "\\usepackage[russian]{babel}\n"
                      "\n"
                      "\\usepackage{xcolor}\n"
                      "\n"
                      "\\usepackage{amsmath}\n"
                      "\\usepackage{amssymb}\n"
                      "\n"
                      "\\begin{document}\n"
                      "\n"
                      "\n")
        self.level = 0

    @staticmethod
    def to_latex_string(string):
        latex_string = string.replace("{", "\\{").replace("}", "\\}")
        i = latex_string.find("_")
        while i != -1:
            d = latex_string[i + 1:].split(None, 1)
            if len(d) == 1:
                latex_string = latex_string[:i + 1] + "{" + latex_string[i + 1:] + "}"
            else:
                latex_string = latex_string[:i + 1] + "{" + d[0] + "} " + d[1]
            i = latex_string.find("_", i + 2)
        return latex_string

    @staticmethod
    def get_style_word(word):
        return "\\text{\\color{blue} \\textbf{%s}}" % word

    @staticmethod
    def split_string(string):
        begin = 0
        formula_sub = []
        for s in re.findall("[!-~]+", string):
            i = string.find(s, begin)
            formula_sub.append((i, i + len(s)))
            begin = formula_sub[-1][1]
        if len(formula_sub) == 0:
            return [(string, 0)]
        full_formula_sub = [formula_sub[0]]
        for i in range(1, len(formula_sub)):
            sub = string[formula_sub[i - 1][1]:formula_sub[i][0]]
            if sub.isspace():
                full_formula_sub[-1] = (full_formula_sub[-1][0], formula_sub[i][1])
            else:
                full_formula_sub.append(formula_sub[i])
        result_split = []
        if full_formula_sub[0][0] > 0:
            result_split.append((string[0:full_formula_sub[0][0]], 0))
        for i in range(len(full_formula_sub) - 1):
            result_split.append((string[full_formula_sub[i][0]:full_formula_sub[i][1]], 1))
            result_split.append((string[full_formula_sub[i][1]:full_formula_sub[i + 1][0]], 0))
        result_split.append((string[full_formula_sub[-1][0]:full_formula_sub[-1][1]], 1))
        if full_formula_sub[-1][1] < len(string):
            result_split.append((string[full_formula_sub[-1][1]:len(string)], 0))
        return result_split

    def print_text(self, text, begin_text, additional_text=""):
        split = self.split_string(text)
        i = 0
        if split[0][1] == 1:
            self.latex += "\\text{%s{%s}} " % (additional_text, begin_text)
        else:
            self.latex += "\\text{%s{%s%s}} " % (additional_text, begin_text, split[0][0])
            i = 1
        for j in range(i, len(split)):
            latex_text = self.to_latex_string(split[j][0]) if split[j][1] == 1 else split[j][0]
            self.latex += ("\\text" if split[j][1] == 0 else "") + "{%s{%s}} " % (additional_text, latex_text)

    def visitMapy(self, ctx):
        self.latex += "$"
        self.visitChildren(ctx)
        self.latex += " $\n\n\\end{document}\n"

    def visitTypedef(self, ctx):
        self.visit(ctx.identifier())
        self.latex += " = "
        self.visit(ctx.structureType())

    def visitCommentLine(self, ctx):
        self.print_text(ctx.getText()[2:], "//", "\\color{gray} ")

    def visitNewline(self, ctx):
        if self.latex[-1] == "$":
            self.latex += " "
        self.latex += "$\n\n$" + "\\quad " * self.level

    def visitFunctionInput(self, ctx):
        text = ctx.getText()
        self.print_text(text[5:], "\\textbf{%s}" % text[:5])

    def visitFunctionOutput(self, ctx):
        text = ctx.getText()
        self.print_text(text[6:], "\\textbf{%s}" % text[:6])

    def visitFunctionDeclaration(self, ctx):
        self.latex += self.get_style_word("func ")
        self.level += 1
        self.visitChildren(ctx)
        self.level -= 1
        self.latex = self.latex[:-6] + self.get_style_word("end func ")

    def visitIdentifier(self, ctx):
        self.latex += "%s" % self.to_latex_string(ctx.getText())

    def visitChildrenDelimiter(self, children, delimiter=",\ "):
        self.visit(children[0])
        for i in range(1, len(children)):
            self.latex += "%s" % delimiter
            self.visit(children[i])

    def visitFormalParameterList(self, ctx):
        self.latex += "("
        self.visitChildrenDelimiter(ctx.parameter())
        self.latex += ") "

    def visitParameter(self, ctx):
        self.visit(ctx.identifier())
        self.latex += "\ :\ "
        self.visit(ctx.typeIdentifier())

    def visitTypeIdentifierList(self, ctx):
        self.latex += ":\ "
        self.visitChildrenDelimiter(ctx.typeIdentifier())

    def visitTypeIdentifier(self, ctx):
        if ctx.identifier() is not None:
            self.latex += self.get_style_word("%s" % self.to_latex_string(ctx.getText()))
        elif ctx.typeT() is not None:
            self.visitChildren(ctx)
        else:
            self.latex += self.get_style_word("%s" % ctx.getText())

    def visitTypeT(self, ctx):
        if ctx.arrayType() is None and ctx.subrangeType() is None:
            self.latex += self.get_style_word("%s" % ctx.getText())
        else:
            self.visitChildren(ctx)

    def visitSubrangeType(self, ctx):
        self.visitChildrenDelimiter(ctx.expression(), "..")

    def visitSubrangeTypeList(self, ctx):
        self.visitChildrenDelimiter(ctx.subrangeType())

    def visitArrayType(self, ctx):
        self.latex += self.get_style_word("array ") + "["
        self.visit(ctx.children[2])
        self.latex += "]" + self.get_style_word(" of ")
        self.visit(ctx.children[5])

    def visitStructureType(self, ctx):
        self.latex += self.get_style_word("struct ") + "\\{"
        self.visit(ctx.children[2])
        self.latex += "\\}"

    def visitStructureTypeList(self, ctx):
        for child in ctx.children:
            if isinstance(child, TerminalNode):
                self.latex += self.get_style_word("%s " % child.getText())
            else:
                self.visit(child)

    def visitSimpleStatement(self, ctx):
        self.visitChildrenDelimiter(ctx.smallStatement(), ";\ ")
        self.latex += "\ "
        if ctx.commentLine() is not None:
            self.visit(ctx.commentLine())

    def visitIdentifierList(self, ctx):
        self.visitChildrenDelimiter(ctx.identifier())

    def visitGlobalStatement(self, ctx):
        self.latex += self.get_style_word("global ")
        self.visit(ctx.identifierList())

    def visitArrowStatement(self, ctx):
        self.visitChildrenDelimiter([ctx.identifier(), ctx.variable()], " %s " % ctx.children[1].getText())

    def visitSwapStatement(self, ctx):
        self.visitChildrenDelimiter(ctx.variable(), " %s " % ctx.children[1].getText())

    def visitSelectStatement(self, ctx):
        self.latex += self.get_style_word("select ")
        self.visit(ctx.identifier())
        self.latex += "\ \\in\ "
        self.visit(ctx.variable())

    def visitBreakStatement(self, ctx):
        self.latex += self.get_style_word("break")

    def visitContinueStatement(self, ctx):
        self.latex += self.get_style_word("continue")

    def visitReturnStatement(self, ctx):
        self.latex += self.get_style_word("return")
        if len(ctx.children) > 1:
            self.latex += "\ "
            if ctx.FAIL() is not None:
                self.latex += self.get_style_word("fail")
            else:
                self.visit(ctx.parameterList())

    def visitYieldStatement(self, ctx):
        self.latex += self.get_style_word("yield ")
        self.visit(ctx.parameterList())

    def visitStopStatement(self, ctx):
        self.latex += self.get_style_word("stop")

    def visitParameterList(self, ctx):
        self.visitChildrenDelimiter(ctx.expression())

    def visitFunctionDesignator(self, ctx):
        if ctx.identifier() is not None:
            self.visit(ctx.identifier())
        else:
            self.latex += "\\text{%s}" % ctx.children[0].getText()
        self.latex += "("
        if ctx.parameterList() is not None:
            self.visit(ctx.parameterList())
        self.latex += ")"

    def visitAssignmentStatement(self, ctx):
        self.visit(ctx.variable())
        self.latex += " := "
        self.visit(ctx.children[2])

    def visitTopExpression(self, ctx):
        self.latex += self.get_style_word("top ")
        self.visit(ctx.variable())

    def visitSetExpression(self, ctx):
        if ctx.emptySet() is not None:
            self.latex += ctx.getText()
        else:
            self.latex += "\\{"
            self.visit(ctx.elementList())
            self.latex += "\\}"

    def visitElementList(self, ctx):
        self.visitChildrenDelimiter(ctx.element())

    def visitElement(self, ctx):
        if len(ctx.children) > 1:
            self.visitChildrenDelimiter(ctx.expression(), "..")
        else:
            self.visit(ctx.expression(0))

    def visitVariable(self, ctx):
        self.visit(ctx.identifier(0))
        for child in ctx.children[1:]:
            if isinstance(child, TerminalNode):
                self.latex += child.getText()
            else:
                self.visit(child)

    def visitExpression(self, ctx):
        self.visit(ctx.orExpression())
        if ctx.expression() is not None:
            self.latex += "\ %s\ " % ctx.relationalOperator().getText()
            self.visit(ctx.expression())

    def visitOrExpression(self, ctx):
        self.visit(ctx.xorExpression())
        if ctx.orExpression() is not None:
            self.latex += "\ %s\ " % ctx.orOperator().getText()
            self.visit(ctx.orExpression())

    def visitXorExpression(self, ctx):
        self.visit(ctx.andExpression())
        if ctx.xorExpression() is not None:
            self.latex += "\ %s\ " % ctx.xorOperator().getText()
            self.visit(ctx.xorExpression())

    def visitAndExpression(self, ctx):
        self.visit(ctx.additiveExpression())
        if ctx.andExpression() is not None:
            self.latex += "\ %s\ " % ctx.andOperator().getText().replace("&", "\\&")
            self.visit(ctx.andExpression())

    def visitAdditiveExpression(self, ctx):
        self.visit(ctx.multiplicativeExpression())
        if ctx.additiveExpression() is not None:
            self.latex += "\ %s\ " % ctx.additiveOperator().getText()
            self.visit(ctx.additiveExpression())

    def visitMultiplicativeExpression(self, ctx):
        self.visit(ctx.signedFactor())
        if ctx.multiplicativeExpression() is not None:
            op = ctx.multiplicativeOperator().children[0]
            if op.symbol.type in [MAPYParser.MOD, MAPYParser.DIV]:
                op = self.get_style_word(" %s " % op.getText())
            else:
                op = "\ %s\ " % op.getText()
            self.latex += op
            self.visit(ctx.multiplicativeExpression())

    def visitSignedFactor(self, ctx):
        if ctx.sign() is not None:
            self.latex += ctx.sign().getText()
        self.visit(ctx.powerFactor())

    def visitPowerFactor(self, ctx):
        self.visit(ctx.factor())
        if ctx.powerFactor() is not None:
            self.latex += " %s " % ctx.powerOperator().getText()
            self.visit(ctx.powerFactor())

    def visitFactor(self, ctx):
        if ctx.expression() is not None:
            self.latex += "("
            self.visit(ctx.expression())
            self.latex += ")"
        elif ctx.unsignedConstant() is not None:
            self.latex += ctx.children[0].getText()
        else:
            self.visitChildren(ctx)

    def visitLengthExpression(self, ctx):
        self.latex += "|"
        self.visit(ctx.expression())
        self.latex += "|"

    def visitRoundExpression(self, ctx):
        self.latex += "%s " % ctx.children[0].getText()
        self.visit(ctx.expression())
        self.latex += " %s" % ctx.children[2].getText()

    def visitStructuredStatement(self, ctx):
        self.visit(ctx.children[0])
        if len(ctx.children) > 1:
            self.latex += " "
            self.visit(ctx.commentLine())

    def visitIfStatement(self, ctx):
        for child in ctx.children:
            if isinstance(child, TerminalNode):
                if child.symbol.type == MAPYParser.IF:
                    self.latex += self.get_style_word("if ")
                elif child.symbol.type in [MAPYParser.ELSE, MAPYParser.ELSEIF, MAPYParser.END]:
                    if self.latex.endswith("\\quad "):
                        self.latex = self.latex[:-6]
                    self.latex += self.get_style_word("%s " % child.getText())
                else:
                    self.latex += self.get_style_word(" then ")
            else:
                if isinstance(child, MAPYParser.SuiteContext):
                    self.level += 1
                    self.visit(child)
                    self.level -= 1
                elif isinstance(child, MAPYParser.NewlineContext):
                    self.visit(child)
                    self.latex += "\\quad "
                else:
                    self.visit(child)

    def visitWhileStatement(self, ctx):
        self.latex += self.get_style_word("while ")
        self.visit(ctx.expression())
        self.latex += self.get_style_word(" do ")
        self.level += 1
        self.visit(ctx.children[3])
        self.level -= 1
        if self.latex.endswith("\\quad "):
            self.latex = self.latex[:-6]
        self.latex += self.get_style_word("end while")

    def visitRepeatStatement(self, ctx):
        self.latex += self.get_style_word("repeat ")
        self.level += 1
        self.visit(ctx.children[1])
        self.level -= 1
        if self.latex.endswith("\\quad "):
            self.latex = self.latex[:-6]
        self.latex += self.get_style_word("until ")
        self.visit(ctx.expression())

    def visitForStatement(self, ctx):
        self.latex += self.get_style_word("for ")
        self.visit(ctx.children[1])
        self.latex += self.get_style_word(" do ")
        self.level += 1
        self.visit(ctx.children[3])
        self.level -= 1
        if self.latex.endswith("\\quad "):
            self.latex = self.latex[:-6]
        self.latex += self.get_style_word("end for")

    def visitForInStatement(self, ctx):
        self.visit(ctx.identifier())
        self.latex += "\ \\in\ "
        self.visit(ctx.variable())

    def visitForToStatement(self, ctx):
        self.visit(ctx.identifier())
        self.latex += self.get_style_word(" from ")
        self.visitChildrenDelimiter(ctx.expression(), self.get_style_word(" %s " % ctx.children[3].getText()))
