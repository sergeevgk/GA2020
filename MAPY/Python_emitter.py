import sys

from antlr4 import TerminalNode

from MAPYVisitor import MAPYVisitor
from MAPYParser import MAPYParser
from var_table import VarTable, Block


class PythonEmitter(MAPYVisitor):
    python: str
    imports: set
    functions: set
    classes: set
    level: int
    table: VarTable
    classes_dict: dict
    var_types: set
    func_types: dict
    logs: list

    types = {'integer': 'int', 'real': 'float', 'char': 'str', 'string': 'str', 'array': 'list'}
    ops = {'\\in': 'in', '\\notin': 'not in', '=': '==', '\\neq': '!=', '\\leq': '<=', '\\geq': '>=',
           '\\^': '^', '&': 'and', '\\vee': 'or', 'mod': '%', 'div': '//', '^': '**'}
    rounds = {'\\lfloor': 'math.floor', '\\lceil': 'math.ceil', '[': 'round'}
    funcs = {'select': 'def select(it):\n\tx = random.sample(it, 1)[0]\n\tit.remove(x)\n\treturn x'}
    default = {'integer': '0', 'int': '0', 'real': '0.0', 'char': '""', 'string': '""'}
    cls = {
        'queue': ('class queue:\n\tarr: list\n\n\tdef __init__(self):\n\t\tself.arr = []\n\n\t'
                  'def enqueue(self, x):\n\t\tself.arr.append(x)\n\n\t'
                  'def dequeue(self):\n\t\treturn self.arr.pop(0)\n\n\t'
                  'def empty(self):\n\t\treturn len(self.arr) == 0\n\n\t'
                  'def clear(self):\n\t\treturn self.arr.clear()'),
        'stack': ('class stack:\n\tarr: list\n\n\tdef __init__(self):\n\t\tself.arr = []\n\n\t'
                  'def push(self, x):\n\t\tself.arr.append(x)\n\n\t'
                  'def pop(self):\n\t\treturn self.arr.pop()\n\n\t'
                  'def top(self):\n\t\treturn self.arr[-1]\n\n\t'
                  'def empty(self):\n\t\treturn len(self.arr) == 0\n\n\t'
                  'def clear(self):\n\t\treturn self.arr.clear()')
    }

    def __init__(self):
        self.python = ""
        self.imports = set()
        self.functions = set()
        self.classes = set()
        self.var_types = {'int', 'float', 'str', 'undef'}
        self.level = 0
        self.table = VarTable()
        self.classes_dict = dict()
        self.func_types = dict()
        self.logs = []

    def add_log(self, string):
        if string not in self.logs:
            self.logs.append(string)

    def add_log_op(self, line, column, type1, op, type2=None):
        if type2 is not None:
            string = f"line {line}:{column} types '{type1}' and '{type2}' are not allowed for the operation '{op}'"
        else:
            string = f"line {line}:{column} type '{type1}' is not allowed for the operation '{op}'"
        self.add_log(string)

    def add_log_undef(self, line, column, undef_name, undef_type):
        self.add_log(f"line {line}:{column} undefined {undef_type} '{undef_name}'")

    def add_log_incorrect_arg(self, line, column):
        self.add_log(f"line {line}:{column} incorrect argument")

    def add_log_string(self, line, column, string):
        self.add_log(f"line {line}:{column} {string}")

    def visitMapy(self, ctx):
        self.table.enter_env()
        self.visitChildren(ctx)
        self.table.exit_env()
        self.python = "".join(map(lambda im: f"import {im}\n", self.imports)) + "\n\n" + \
                      "".join(map(lambda f: f"{self.funcs[f]}\n\n\n", self.functions)) + \
                      "".join(map(lambda cl: f"{self.cls[cl]}\n\n\n", self.classes)) + self.python + "\n"
        self.python = self.python.replace("\t", "    ")
        print(*self.logs, file=sys.stderr, sep="\n")

    def visitTypedef(self, ctx):
        self.python += f"class {ctx.identifier().getText()}:\n"
        self.var_types.add(ctx.identifier().getText())
        self.level += 1
        self.visit(ctx.structureType())
        self.level -= 1

    def visitStructureType(self, ctx):
        self.visit(ctx.children[2])

    def visitStructureTypeList(self, ctx):
        struct_name = ctx.parentCtx.parentCtx.identifier().getText()
        block = Block()
        for parameter in ctx.parameter():
            field_name, field_type_id_ctx = parameter.identifier().getText(), parameter.typeIdentifier()
            field_type_name = self.get_type_identifier_name(field_type_id_ctx)
            block.add_variable(field_name, field_type_name)
            if Block.is_type_structured(field_type_name):
                field_type_name = field_type_name[0]
            self.python += "\t" * self.level + f"{field_name}: {field_type_name}\n"
        self.classes_dict[struct_name] = block

    def visitCommentLine(self, ctx):
        self.python += f"# {ctx.getText()[2:]}"

    def visitNewline(self, ctx):
        self.python += "\n" + "\t" * self.level

    def visitFunctionInput(self, ctx):
        self.python += f"# {ctx.getText()}"

    def visitFunctionOutput(self, ctx):
        self.python += f"# {ctx.getText()}"

    def visitFunctionDeclaration(self, ctx):
        self.python += "def "
        self.level += 1
        self.table.enter_env()
        self.visit(ctx.identifier())
        self.visit(ctx.formalParameterList())
        if ctx.typeIdentifierList() is not None:
            self.visit(ctx.typeIdentifierList())
        else:
            self.func_types[ctx.identifier().getText()] = "undef"
        self.python += ":"
        self.visit(ctx.suite())
        self.level -= 1
        self.table.exit_env()
        i = self.python.rfind("\n")
        if self.python[i + 1:].isspace():
            self.python = self.python[:i]

    def visitIdentifier(self, ctx):
        self.python += f"{ctx.getText()}"

    def visitChildrenDelimiter(self, children, delimiter=", "):
        self.visit(children[0])
        for i in range(1, len(children)):
            self.python += "%s" % delimiter
            self.visit(children[i])

    def visitFormalParameterList(self, ctx):
        self.python += "("
        self.visitChildrenDelimiter(ctx.parameter())
        self.python += ")"

    def is_type_valid(self, var_type):
        return var_type in self.var_types or Block.is_type_structured(var_type)

    def get_type_identifier_name(self, type_id_ctx):
        if type_id_ctx.typeT() is not None and type_id_ctx.typeT().subrangeType() is not None:
            type_id = "int"
        elif type_id_ctx.typeT() is not None and type_id_ctx.typeT().arrayType() is not None:
            type_id = ("list",
                       self.get_type_identifier_name(type_id_ctx.typeT().arrayType().componentType().typeIdentifier()))
        elif type_id_ctx.typeT() is not None and type_id_ctx.typeT().setType() is not None:
            type_id = tuple(["set", "undef"])
        else:
            type_id = type_id_ctx.start.text
            if type_id in self.cls.keys():
                type_id = (type_id, "undef")
        type_name = self.types.get(type_id, type_id)
        if not self.is_type_valid(type_name):
            line, column = type_id_ctx.start.line, type_id_ctx.start.column
            self.add_log_undef(line, column, type_name, "type")
        return type_name

    def get_type_variable(self, var_ctx):
        type_name = self.table.get_type(var_ctx.identifier(0).getText())
        line, column = var_ctx.start.line, var_ctx.start.column
        i = 1
        while i < len(var_ctx.children):
            child = var_ctx.children[i]
            if child.symbol.type == MAPYParser.LBRACK:
                if not Block.is_type_structured(type_name, "list"):
                    self.add_log_op(line, column, type_name, "[]")
                    return "undef"
                type_name = type_name[1]
                i += 3
            else:
                field_name = var_ctx.children[i + 1].getText()
                if not self.classes_dict[type_name].find_variable(field_name):
                    self.add_log_undef(line, column, field_name, "field of structure")
                    return "undef"
                type_name = self.classes_dict[type_name].get_type(field_name)
                i += 2
        return type_name

    def visitParameter(self, ctx):
        self.visit(ctx.identifier())
        var_name = ctx.identifier().getText()
        var_type = self.get_type_identifier_name(ctx.typeIdentifier())
        self.table.add_variable(var_name, var_type)
        if isinstance(ctx.parentCtx, MAPYParser.FormalParameterListContext):
            self.python += ": "
            self.visit(ctx.typeIdentifier())
        else:
            self.python += " = "
            child = ctx.typeIdentifier().children[0]
            if isinstance(child, TerminalNode):
                self.python += self.default[child.getText()]
            elif isinstance(child, MAPYParser.IdentifierContext):
                self.python += f"{child.getText()}()"
            else:
                self.visit(child)

    def visitTypeIdentifierList(self, ctx):
        types = []
        for type_id_ctx in ctx.typeIdentifier():
            types.append(self.get_type_identifier_name(type_id_ctx))
        self.func_types[ctx.parentCtx.identifier().getText()] = tuple(types) if len(types) > 1 else types[0]
        self.python += " -> "
        self.visitChildrenDelimiter(ctx.typeIdentifier())

    def visitTypeIdentifier(self, ctx):
        if ctx.start.text in self.cls.keys():
            self.classes.add(ctx.start.text)
        type_name = self.get_type_identifier_name(ctx)
        if Block.is_type_structured(type_name):
            type_name = type_name[0]
        self.python += type_name

    def visitTypeT(self, ctx):
        if ctx.arrayType() is None and ctx.subrangeType() is None:
            if ctx.getText() in self.cls.keys():
                self.classes.add(ctx.getText())
            self.python += f"{ctx.getText()}()"
        elif ctx.subrangeType() is not None:
            self.python += self.default['int']
        else:
            self.visitChildren(ctx)

    def visitSubrangeType(self, ctx):
        self.python += "[None for _ in range("
        self.visit(ctx.expression(1))
        self.python += " - "
        self.visit(ctx.expression(0))
        self.python += " + 1)]"

    def visitSubrangeTypeList(self, ctx):
        self.visit(ctx.subrangeType(0))
        for child in ctx.subrangeType()[1:]:
            i = self.python.rfind("None")
            residual = self.python[i + 4:]
            self.python = self.python[:i]
            self.visit(child)
            self.python += residual

    def visitArrayType(self, ctx):
        self.visit(ctx.children[2])

    def visitSimpleStatement(self, ctx):
        self.visitChildrenDelimiter(ctx.smallStatement(), "; ")
        self.python += " "
        if ctx.commentLine() is not None:
            self.visit(ctx.commentLine())

    def visitIdentifierList(self, ctx):
        self.visitChildrenDelimiter(ctx.identifier())

    def visitGlobalStatement(self, ctx):
        self.python += "global "
        self.visit(ctx.identifierList())

    def visitArrowStatement(self, ctx):
        var_type = self.get_type_variable(ctx.variable())
        if not Block.is_type_structured(var_type, "queue") and not Block.is_type_structured(var_type, "stack"):
            line, column = ctx.variable().start.line, ctx.variable().start.column
            self.add_log_op(line, column, var_type, ctx.children[1].getText())
        if ctx.children[1].symbol.type == MAPYParser.LARROW:
            self.visitChildrenDelimiter([ctx.identifier(), ctx.variable()], " = ")
            self.table.add_variable(ctx.identifier().getText(), var_type[1])
            func = "pop" if Block.is_type_structured(var_type, "stack") else "dequeue"
            self.python += f".{func}()"
        else:
            func = "push" if Block.is_type_structured(var_type, "stack") else "enqueue"
            self.visitChildrenDelimiter([ctx.variable(), ctx.identifier()], f".{func}(")
            self.python += ")"
            if len(ctx.variable().children) == 1:
                self.table.add_variable(ctx.variable().identifier(0).getText(),
                                        (var_type[0], self.table.get_type(ctx.identifier().getText())))

    def visitSwapStatement(self, ctx):
        self.visitChildrenDelimiter(ctx.variable())
        self.python += " = "
        self.visitChildrenDelimiter(ctx.variable()[::-1])

    def visitSelectStatement(self, ctx):
        self.visit(ctx.identifier())
        self.python += " = select("
        self.visit(ctx.variable())
        self.python += ")"
        var_type = self.get_type_variable(ctx.variable())
        if not Block.is_type_structured(var_type, "list") and not Block.is_type_structured(var_type, "set"):
            line, column = ctx.variable().start.line, ctx.variable().start.column
            self.add_log_op(line, column, var_type, "select")
            self.table.add_variable(ctx.identifier().getText(), "undef")
        else:
            self.table.add_variable(ctx.identifier().getText(), var_type[1])
        self.imports.add("random")
        self.functions.add("select")

    def visitBreakStatement(self, ctx):
        self.python += "break"

    def visitContinueStatement(self, ctx):
        self.python += "continue"

    def visitReturnStatement(self, ctx):
        if ctx.FAIL() is not None:
            self.python += f'raise Exception("{ctx.FAIL().getText()}")'
        else:
            self.python += "return"
            if len(ctx.children) > 1:
                self.python += " "
                self.visit(ctx.parameterList())

    def visitYieldStatement(self, ctx):
        self.python += "yield "
        self.visit(ctx.parameterList())
        if list(self.func_types.values())[-1] == "undef":
            types = []
            for exp_ctx in ctx.parameterList().expression():
                types.append(self.get_type_expression(exp_ctx))
            self.func_types[list(self.func_types.keys())[-1]] = tuple(types) if len(types) > 1 else types[0]

    def visitStopStatement(self, ctx):
        self.python += "exit(0)"

    def visitParameterList(self, ctx):
        self.visitChildrenDelimiter(ctx.expression())

    def visitFunctionDesignator(self, ctx):
        func_name = ctx.children[0].getText()
        if func_name not in ["min", "max"] and func_name not in self.func_types.keys():
            line, column = ctx.start.line, ctx.start.column
            self.add_log_undef(line, column, func_name, "function")
        self.python += func_name
        self.python += "("
        if ctx.parameterList() is not None:
            self.visit(ctx.parameterList())
        self.python += ")"

    def visitAssignmentStatement(self, ctx):
        self.visit(ctx.variable())
        var_name = ctx.variable().identifier(0).getText()
        if ctx.setExpression() is not None and ctx.setExpression().emptySet() is not None and \
                self.table.find_variable(var_name):
            var_type = self.get_type_variable(ctx.variable())
            if Block.is_type_structured(var_type, "queue") or Block.is_type_structured(var_type, "stack") or \
                    Block.is_type_structured(var_type, "set"):
                self.python += ".clear()"
        else:
            self.python += " = "
            self.visit(ctx.children[2])
            if len(ctx.variable().children) == 1:
                if ctx.expression() is not None:
                    self.table.add_variable(var_name, self.get_type_expression(ctx.children[2]))
                elif ctx.setExpression() is not None:
                    self.table.add_variable(var_name, self.get_type_set_expression(ctx.children[2]))
                else:
                    self.table.add_variable(var_name, self.get_type_top_expression(ctx.children[2]))

    def visitTopExpression(self, ctx):
        self.visit(ctx.variable())
        self.python += ".top()"

    def visitSetExpression(self, ctx):
        if ctx.emptySet() is not None:
            self.python += "set()"
        else:
            self.python += "set"
            self.visit(ctx.elementList())

    def visitElementList(self, ctx):
        self.visitChildrenDelimiter(ctx.element(), ".union")

    def visitElement(self, ctx):
        self.python += "("
        if len(ctx.children) > 1:
            self.python += "range("
            self.visitChildrenDelimiter(ctx.expression())
            self.python += " + 1)"
        else:
            self.python += "{"
            self.visit(ctx.expression(0))
            self.python += "}"
        self.python += ")"

    def visitVariable(self, ctx):
        self.visit(ctx.identifier(0))
        for child in ctx.children[1:]:
            if isinstance(child, TerminalNode):
                self.python += child.getText()
            elif isinstance(child, MAPYParser.ParameterListContext):
                expressions = child.expression()
                self.visitChildrenDelimiter(expressions, " - 1][")
                self.python += " - 1"
            else:
                self.visit(child)

    def visitExpression(self, ctx):
        if ctx.expression() is not None:
            op = ctx.relationalOperator().getText()
            if self.get_type_expression(ctx) == "undef":
                self.visit(ctx.orExpression())
                self.python += f" {self.ops.get(op, op)} "
                self.visit(ctx.expression())
            else:
                or_type = self.get_type_or_expression(ctx.orExpression())
                op_type = ctx.relationalOperator().start.type
                if op_type in [MAPYParser.EQUAL, MAPYParser.NOT_EQUAL] and \
                        ctx.expression().start == ctx.expression().stop and \
                        ctx.expression().start.type == MAPYParser.EMPTY_SET:
                    if Block.is_type_structured(or_type, "set"):
                        self.python += f"{'not ' if op_type == MAPYParser.EQUAL else ''}bool("
                        self.visit(ctx.orExpression())
                        self.python += ")"
                    else:
                        self.python += "not" if op_type == MAPYParser.NOT_EQUAL else ""
                        self.visit(ctx.orExpression())
                        self.python += ".empty()"
                else:
                    self.visit(ctx.orExpression())
                    self.python += f" {self.ops.get(op, op)} "
                    self.visit(ctx.expression())
        else:
            self.visit(ctx.orExpression())

    def visitOrExpression(self, ctx):
        self.visit(ctx.xorExpression())
        if ctx.orExpression() is not None:
            op = ctx.orOperator().getText()
            if self.get_type_or_expression(ctx) == "undef":
                self.python += f" {self.ops.get(op, op)} "
                self.visit(ctx.orExpression())
            else:
                xor_type = self.get_type_xor_expression(ctx.xorExpression())
                if Block.is_type_structured(xor_type, "set"):
                    self.python += ".union("
                    self.visit(ctx.orExpression())
                    self.python += ")"
                else:
                    self.python += f" {self.ops.get(op, op)} "
                    self.visit(ctx.orExpression())

    def visitXorExpression(self, ctx):
        self.visit(ctx.andExpression())
        if ctx.xorExpression() is not None:
            op = ctx.xorOperator().getText()
            self.python += f" {self.ops.get(op, op)} "
            self.visit(ctx.xorExpression())

    def visitAndExpression(self, ctx):
        self.visit(ctx.additiveExpression())
        if ctx.andExpression() is not None:
            op = ctx.andOperator().getText()
            if self.get_type_and_expression(ctx) == "undef":
                self.python += f" {self.ops.get(op, op)} "
                self.visit(ctx.andExpression())
            else:
                op_type = ctx.andOperator().start.type
                add_type = self.get_type_add_expression(ctx.additiveExpression())
                if Block.is_type_structured(add_type, "set"):
                    if op_type == MAPYParser.INTERSECTION:
                        self.python += ".intersection("
                        self.visit(ctx.andExpression())
                        self.python += ")"
                    else:
                        self.python += ".difference("
                        self.visit(ctx.andExpression())
                        self.python += ")"
                else:
                    self.python += f" {self.ops.get(op, op)} "
                    self.visit(ctx.andExpression())

    def visitAdditiveExpression(self, ctx):
        self.visit(ctx.multiplicativeExpression())
        if ctx.additiveExpression() is not None:
            op = ctx.additiveOperator().getText()
            if self.get_type_add_expression(ctx) == "undef":
                self.python += f" {self.ops.get(op, op)} "
                self.visit(ctx.additiveExpression())
            else:
                op_type = ctx.additiveOperator().start.type
                mult_type = self.get_type_mult_expression(ctx.multiplicativeExpression())
                if Block.is_type_structured(mult_type, "set"):
                    if op_type == MAPYParser.MINUS:
                        self.python += ".difference({"
                        self.visit(ctx.additiveExpression())
                        self.python += "})"
                    else:
                        self.python += ".union({"
                        self.visit(ctx.additiveExpression())
                        self.python += "})"
                else:
                    self.python += f" {self.ops.get(op, op)} "
                    self.visit(ctx.additiveExpression())

    def visitMultiplicativeExpression(self, ctx):
        self.visit(ctx.signedFactor())
        if ctx.multiplicativeExpression() is not None:
            op = ctx.multiplicativeOperator().getText()
            self.python += f" {self.ops.get(op, op)} "
            self.visit(ctx.multiplicativeExpression())

    def visitSignedFactor(self, ctx):
        if ctx.sign() is not None:
            self.python += ctx.sign().getText()
        self.visit(ctx.powerFactor())

    def visitPowerFactor(self, ctx):
        self.visit(ctx.factor())
        if ctx.powerFactor() is not None:
            op = ctx.powerOperator().getText()
            self.python += f" {self.ops.get(op, op)} "
            self.visit(ctx.powerFactor())

    def visitFactor(self, ctx):
        if ctx.expression() is not None:
            self.python += "("
            self.visit(ctx.expression())
            self.python += ")"
        elif ctx.unsignedConstant() is not None:
            const = ctx.unsignedConstant()
            if const.unsignedNumber() is not None and const.unsignedNumber().unsignedReal() is not None and \
                    const.unsignedNumber().unsignedReal().INFINITY is not None:
                self.python += 'float("inf")'
            elif const.string() is not None and const.string().EMPTY_STRING() is not None:
                self.python += '""'
            else:
                self.python += const.getText()
        else:
            self.visitChildren(ctx)

    def visitLengthExpression(self, ctx):
        self.python += "len("
        self.visit(ctx.expression())
        self.python += ")"

    def visitRoundExpression(self, ctx):
        self.python += f"{self.rounds[ctx.children[0].getText()]}("
        self.visit(ctx.expression())
        self.python += ")"
        self.imports.add("math")

    def visitStructuredStatement(self, ctx):
        self.visit(ctx.children[0])
        if len(ctx.children) > 1:
            self.python += " "
            self.visit(ctx.commentLine())

    def visitIfStatement(self, ctx):
        self.python += "if "
        for child in ctx.children[1:-2]:
            if isinstance(child, TerminalNode):
                if child.symbol.type in [MAPYParser.ELSE, MAPYParser.ELSEIF]:
                    if self.python.endswith("\t"):
                        self.python = self.python[:-1]
                    if child.getText() == "elseif":
                        self.python += "elif "
                    else:
                        self.python += "else: "
                else:
                    self.python += ": "
            else:
                if isinstance(child, MAPYParser.SuiteContext):
                    self.level += 1
                    self.visit(child)
                    self.level -= 1
                elif isinstance(child, MAPYParser.NewlineContext):
                    self.visit(child)
                    self.python += "\t"
                else:
                    self.get_type_expression(child)
                    self.visit(child)
        i = self.python.rfind("\n")
        if self.python[i + 1:].isspace():
            self.python = self.python[:i]

    def visitWhileStatement(self, ctx):
        self.python += "while "
        self.visit(ctx.expression())
        self.python += ": "
        self.level += 1
        self.visit(ctx.children[3])
        self.level -= 1
        i = self.python.rfind("\n")
        if self.python[i + 1:].isspace():
            self.python = self.python[:i]

    def visitRepeatStatement(self, ctx):
        self.python += "while True: "
        self.level += 1
        self.visit(ctx.children[1])
        self.level -= 1
        self.python += "if "
        self.visit(ctx.expression())
        self.python += ": break"

    def visitForStatement(self, ctx):
        self.python += "for "
        self.visit(ctx.children[1])
        self.python += ": "
        self.level += 1
        self.visit(ctx.children[3])
        self.level -= 1
        i = self.python.rfind("\n")
        if self.python[i + 1:].isspace():
            self.python = self.python[:i]

    def visitForInStatement(self, ctx):
        self.visit(ctx.identifier())
        self.python += " in "
        self.visit(ctx.variable())
        var_type = self.get_type_variable(ctx.variable())
        if Block.is_type_structured(var_type, "list") or Block.is_type_structured(var_type, "set"):
            self.table.add_variable(ctx.identifier().getText(), var_type[1])
        else:
            line, column = ctx.variable().start.line, ctx.variable().start.column
            self.add_log_op(line, column, var_type, "for...in...")
            self.table.add_variable(ctx.identifier().getText(), "undef")

    def visitForToStatement(self, ctx):
        self.visit(ctx.identifier())
        self.python += " in range("
        self.visitChildrenDelimiter(ctx.expression())
        step = 1 if ctx.children[3].symbol.type == MAPYParser.TO else -1
        self.python += f" + {step}, {step})"
        self.table.add_variable(ctx.identifier().getText(), "int")

    def get_type_set_expression(self, ctx):
        if ctx.emptySet() is not None:
            return tuple(["set", "undef"])
        else:
            return tuple(["set", self.get_type_element_list(ctx.elementList())])

    def get_type_element_list(self, ctx):
        types = set()
        for element in ctx.element():
            types.add(self.get_type_element(element))
        types = list(types)
        if len(types) == 1:
            return types[0]
        elif len(types) == 2 and "undef" in types:
            return types[0] if types[0] != "undef" else types[1]
        return "undef"

    def get_type_element(self, ctx):
        exp_type0 = self.get_type_expression(ctx.expression(0))
        if ctx.expression(1) is not None:
            exp_type1 = self.get_type_expression(ctx.expression(1))
            if exp_type0 != exp_type1:
                line, column = ctx.start.line, ctx.start.column
                self.add_log_string(line, column, "types of limits of the range are not compatible")
                return exp_type0 if exp_type0 != "undef" else exp_type1
        return exp_type0

    def get_type_unsigned_number(self, ctx):
        return "int" if ctx.unsignedInteger() is not None else "float"

    def get_type_unsigned_const(self, ctx):
        return self.get_type_unsigned_number(ctx.unsignedNumber()) if ctx.unsignedNumber() is not None else "str"

    def get_type_parameter_list(self, ctx):
        types = []
        for exp in ctx.expression():
            types.append(self.get_type_expression(exp))
        return tuple(types) if len(types) > 1 else types[0]

    def get_type_func(self, ctx):
        func_name = ctx.children[0].getText()
        func_type = "undef"
        if func_name in self.func_types.keys():
            func_type = self.func_types[func_name]
        if func_name in ["min", "max"]:
            if ctx.parameterList() is None:
                line, column = ctx.start.line, ctx.start.column + 3
                self.add_log_incorrect_arg(line, column)
                return "undef"
            args_type = self.get_type_parameter_list(ctx.parameterList())
            if len(args_type) < 2 or (not Block.is_type_structured(args_type, "set") and
                                      not Block.is_type_structured(args_type, "list") and
                                      ((len(set(args_type)) == 2 and "undef" not in set(args_type)) or
                                       len(set(args_type)) > 1)):
                line, column = ctx.parameterList().start.line, ctx.parameterList().start.column
                self.add_log_incorrect_arg(line, column)
                return "undef"
            if Block.is_type_structured(args_type, "set") or Block.is_type_structured(args_type, "list"):
                return args_type[1]
            args_type = list(set(args_type))
            if len(args_type) == 1:
                return args_type[0]
            return args_type[0] if args_type[0] != "undef" else args_type[1]
        if func_type == "undef":
            line, column = ctx.start.line, ctx.start.column
            self.add_log_string(line, column, "returned type of function is undefined")
            return "undef"
        return func_type

    def get_type_len_expression(self, ctx):
        exp_type = self.get_type_expression(ctx.expression())
        if exp_type == "str" or Block.is_type_structured(exp_type, "list") or Block.is_type_structured(exp_type, "set"):
            return "int"
        line, column = ctx.expression().start.line, ctx.expression().start.column
        self.add_log_op(line, column, exp_type, "||")
        return "undef"

    def get_type_round_expression(self, ctx):
        exp_type = self.get_type_expression(ctx.expression())
        if exp_type not in ["int", "float"]:
            line, column = ctx.expression().start.line, ctx.expression().start.column
            self.add_log_op(line, column, exp_type, "round")
            return "undef"
        return "int"

    def get_type_factor(self, ctx):
        if ctx.variable() is not None:
            return self.get_type_variable(ctx.variable())
        elif ctx.expression() is not None:
            return self.get_type_expression(ctx.expression())
        elif ctx.roundExpression() is not None:
            return self.get_type_round_expression(ctx.roundExpression())
        elif ctx.lengthExpression() is not None:
            return self.get_type_len_expression(ctx.lengthExpression())
        elif ctx.functionDesignator() is not None:
            return self.get_type_func(ctx.functionDesignator())
        elif ctx.unsignedConstant() is not None:
            return self.get_type_unsigned_const(ctx.unsignedConstant())
        else:
            return self.get_type_set_expression(ctx.setExpression())

    def get_type_pow_factor(self, ctx):
        factor_type = self.get_type_factor(ctx.factor())
        if ctx.powerFactor() is not None:
            pow_factor_type = self.get_type_pow_factor(ctx.powerFactor())
            op = ctx.powerOperator().getText()
            if pow_factor_type not in ["int", "float"]:
                line, column = ctx.powerFactor().start.line, ctx.powerFactor().start.column
                self.add_log_op(line, column, pow_factor_type, op)
                return "undef"
            if factor_type not in ["int", "float"]:
                line, column = ctx.factor().start.line, ctx.factor().start.column
                self.add_log_op(line, column, factor_type, op)
                return "undef"
            return "int" if factor_type == pow_factor_type == "int" else "float"
        return factor_type

    def get_type_sign_factor(self, ctx):
        pow_factor_type = self.get_type_pow_factor(ctx.powerFactor())
        if ctx.sign() is not None:
            op = ctx.sign().getText()
            if pow_factor_type not in ["int", "float"]:
                line, column = ctx.powerFactor().start.line, ctx.powerFactor().start.column
                self.add_log_op(line, column, pow_factor_type, op)
                return "undef"
        return pow_factor_type

    def get_type_mult_expression(self, ctx):
        sign_factor_type = self.get_type_sign_factor(ctx.signedFactor())
        if ctx.multiplicativeExpression() is not None:
            mult_exp_type = self.get_type_mult_expression(ctx.multiplicativeExpression())
            op = ctx.multiplicativeOperator().getText()
            if mult_exp_type not in ["int", "float"]:
                line, column = ctx.multiplicativeExpression().start.line, \
                               ctx.multiplicativeExpression().start.column
                self.add_log_op(line, column, mult_exp_type, op)
                return "undef"
            if sign_factor_type not in ["int", "float"]:
                line, column = ctx.signedFactor().start.line, ctx.signedFactor().start.column
                self.add_log_op(line, column, sign_factor_type, op)
                return "undef"
            return "float" if mult_exp_type == "float" or sign_factor_type == "float" else "int"
        return sign_factor_type

    def get_type_add_expression(self, ctx):
        mult_exp_type = self.get_type_mult_expression(ctx.multiplicativeExpression())
        if ctx.additiveExpression() is not None:
            add_exp_type = self.get_type_add_expression(ctx.additiveExpression())
            op = ctx.additiveOperator().getText()
            if add_exp_type not in ["int", "float", "str"] and not Block.is_type_structured(add_exp_type, "list"):
                line, column = ctx.additiveExpression().start.line, ctx.additiveExpression().start.column
                self.add_log_op(line, column, add_exp_type, op)
                return "undef"
            if mult_exp_type not in ["int", "float", "str"] and not Block.is_type_structured(mult_exp_type, "list") \
                    and not Block.is_type_structured(mult_exp_type, "set"):
                line, column = ctx.multiplicativeExpression().start.line, \
                               ctx.multiplicativeExpression().start.column
                self.add_log_op(line, column, mult_exp_type, op)
                return "undef"
            if (Block.is_type_structured(mult_exp_type, "list") and not Block.is_type_structured(add_exp_type, "list"))\
                    or (mult_exp_type == "str" and add_exp_type != "str") or \
                    (Block.is_type_structured(mult_exp_type, "set") and add_exp_type != mult_exp_type[1]):
                line, column = ctx.additiveOperator().start.line, ctx.additiveOperator().start.column
                self.add_log_op(line, column, mult_exp_type, op, add_exp_type)
                return "undef"
            op_type = ctx.additiveOperator().start.type
            if op_type == MAPYParser.MINUS and \
                    ((Block.is_type_structured(mult_exp_type, "list") or mult_exp_type == "str") or
                     (mult_exp_type in ["int", "float"] and add_exp_type not in ["int", "float"])):
                line, column = ctx.additiveOperator().start.line, ctx.additiveOperator().start.column
                self.add_log_op(line, column, mult_exp_type, op, add_exp_type)
                return "undef"
            if Block.is_type_structured(mult_exp_type, "list") or mult_exp_type == "str" or \
                    Block.is_type_structured(mult_exp_type, "set"):
                return mult_exp_type
            return "float" if "float" in [mult_exp_type, add_exp_type] else "int"
        return mult_exp_type

    def get_type_and_expression(self, ctx):
        add_exp_type = self.get_type_add_expression(ctx.additiveExpression())
        if ctx.andExpression() is not None:
            and_exp_type = self.get_type_and_expression(ctx.andExpression())
            op_type = ctx.andOperator().start.type
            op = ctx.andOperator().getText()
            if op_type == MAPYParser.AND:
                if and_exp_type not in ["int", "bool"]:
                    line, column = ctx.andExpression().start.line, ctx.andExpression().start.column
                    self.add_log_op(line, column, and_exp_type, op)
                    return "undef"
                if add_exp_type not in ["int", "bool"]:
                    line, column = ctx.additiveExpression().start.line, ctx.additiveExpression().start.column
                    self.add_log_op(line, column, add_exp_type, op)
                    return "undef"
                return "int" if "int" in [add_exp_type, and_exp_type] else "bool"
            else:
                if and_exp_type != add_exp_type or not Block.is_type_structured(add_exp_type, "set"):
                    line, column = ctx.andOperator().start.line, ctx.andOperator().start.column
                    self.add_log_op(line, column, add_exp_type, op, and_exp_type)
                    return "undef"
                return add_exp_type
        return add_exp_type

    def get_type_xor_expression(self, ctx):
        and_exp_type = self.get_type_and_expression(ctx.andExpression())
        if ctx.xorExpression() is not None:
            xor_exp_type = self.get_type_xor_expression(ctx.xorExpression())
            op = ctx.xorOperator().getText()
            if xor_exp_type not in ["int", "bool"]:
                line, column = ctx.xorExpression().start.line, ctx.xorExpression().start.column
                self.add_log_op(line, column, xor_exp_type, op)
                return "undef"
            if and_exp_type not in ["int", "bool"]:
                line, column = ctx.andExpression().start.line, ctx.andExpression().start.column
                self.add_log_op(line, column, and_exp_type, op)
                return "undef"
            return "int"
        return and_exp_type

    def get_type_or_expression(self, ctx):
        xor_exp_type = self.get_type_xor_expression(ctx.xorExpression())
        if ctx.orExpression() is not None:
            or_exp_type = self.get_type_or_expression(ctx.orExpression())
            op_type = ctx.orOperator().start.type
            op = ctx.orOperator().getText()
            if op_type == MAPYParser.OR:
                if or_exp_type not in ["int", "bool"]:
                    line, column = ctx.orExpression().start.line, ctx.orExpression().start.column
                    self.add_log_op(line, column, or_exp_type, op)
                    return "undef"
                if xor_exp_type not in ["int", "bool"]:
                    line, column = ctx.xorExpression().start.line, ctx.xorExpression().start.column
                    self.add_log_op(line, column, xor_exp_type, op)
                    return "undef"
                return "int" if "int" in [xor_exp_type, or_exp_type] else "bool"
            else:
                if or_exp_type != xor_exp_type or not Block.is_type_structured(xor_exp_type, "set"):
                    line, column = ctx.orOperator().start.line, ctx.orOperator().start.column
                    self.add_log_op(line, column, xor_exp_type, op, or_exp_type)
                    return "undef"
                return xor_exp_type
        return xor_exp_type

    def get_type_expression(self, ctx):
        or_exp_type = self.get_type_or_expression(ctx.orExpression())
        if ctx.expression() is not None:
            exp_type = self.get_type_expression(ctx.expression())
            op_type = ctx.relationalOperator().children[0].symbol.type
            op = ctx.relationalOperator().getText()
            if op_type in [MAPYParser.LT, MAPYParser.LE, MAPYParser.GE, MAPYParser.GT]:
                if exp_type != or_exp_type or exp_type not in ["int", "float", "str"]:
                    line, column = ctx.relationalOperator().start.line, ctx.relationalOperator().start.column
                    self.add_log_op(line, column, or_exp_type, op, exp_type)
                    return "undef"
            if op_type in [MAPYParser.IN, MAPYParser.NOT_IN]:
                if (exp_type == "str" and or_exp_type != "str") or Block.is_type_structured(exp_type, "queue") or \
                        Block.is_type_structured(exp_type, "stack") or \
                        ((Block.is_type_structured(exp_type, "set") or Block.is_type_structured(exp_type, "list")) and
                         or_exp_type != exp_type[1]):
                    line, column = ctx.relationalOperator().start.line, ctx.relationalOperator().start.column
                    self.add_log_op(line, column, or_exp_type, op, exp_type)
                    return "undef"
            if op_type in [MAPYParser.EQUAL, MAPYParser.NOT_EQUAL] and ctx.expression().start == ctx.expression().stop \
                    and ctx.expression().start.type == MAPYParser.EMPTY_SET:
                if not Block.is_type_structured(or_exp_type, "set") and \
                        not Block.is_type_structured(or_exp_type, "queue") and \
                        not Block.is_type_structured(or_exp_type, "stack"):
                    line, column = ctx.orExpression().start.line, ctx.orExpression().start.column
                    self.add_log_op(line, column, or_exp_type, f"{op} {ctx.expression().getText()}")
                    return "undef"
            return "bool"
        return or_exp_type

    def get_type_top_expression(self, ctx):
        var_type = self.get_type_variable(ctx.variable())
        if not Block.is_type_structured(var_type, "stack"):
            line, column = ctx.variable().start.line, ctx.variable().start.column
            self.add_log_op(line, column, var_type, "top")
            return "undef"
        return var_type[1]
