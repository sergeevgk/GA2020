from enum import Enum


class LexemType(Enum):
	COMMA = 0
	SEMICOLON = 1
	SHARP = 2

	STRING_CONST = 4

	ROUND_BRACKET_OPEN = 60
	ROUND_BRACKET_CLOSE = 61
	FIGURE_BRACKET_OPEN = 62
	FIGURE_BRACKET_CLOSE = 63
	TRIANGLE_BRACKET_OPEN = 64
	TRIANGLE_BRACKET_CLOSE = 65
	SQUARE_BRACKET_OPEN = 66
	SQUARE_BRACKET_CLOSE = 67

	QUOTE_DOUBLE = 7
	QUOTE = 8

	FOR = 10
	IF = 11
	WHILE = 12
	ELSE = 13
	
	DATA_TYPE = 20

	BIN_OP = 30

	ASSIGN = 70

	VARIABLE = 40
	NUMBER = 41
	FUNC_CALL = 42

	INCLUDE = 50
	RETURN = 51

	OTHER = 100


symbols = ['+', '=', '-', '*', '&', '|', '<', '>']

quotes = {
			'\"': LexemType.QUOTE_DOUBLE,
			'\'': LexemType.QUOTE
}

separators = {
				'(': LexemType.ROUND_BRACKET_OPEN,
				')': LexemType.ROUND_BRACKET_CLOSE,
				'{': LexemType.FIGURE_BRACKET_OPEN,
				'}': LexemType.FIGURE_BRACKET_CLOSE,
				'[': LexemType.SQUARE_BRACKET_OPEN,
				']': LexemType.SQUARE_BRACKET_CLOSE,
				';': LexemType.SEMICOLON,
				',': LexemType.COMMA,
				'#': LexemType.SHARP,
				'<': LexemType.TRIANGLE_BRACKET_OPEN,
				'>': LexemType.TRIANGLE_BRACKET_CLOSE,
}

keywords = {
			'for': LexemType.FOR,
			'while': LexemType.WHILE,
			'if': LexemType.IF,
			'else': LexemType.ELSE,
			'include': LexemType.INCLUDE,
			'return': LexemType.RETURN
}

operators = {
			'+': LexemType.BIN_OP,
			'==': LexemType.BIN_OP,
			'-': LexemType.BIN_OP,
			'*': LexemType.BIN_OP,
			'&&': LexemType.BIN_OP,
			'||': LexemType.BIN_OP
}

assign = {
		'=': LexemType.ASSIGN,
		'+=': LexemType.ASSIGN,
		'-=': LexemType.ASSIGN,
		'*=': LexemType.ASSIGN
}

types = {
		'int': LexemType.DATA_TYPE,
		'char': LexemType.DATA_TYPE,
		'double': LexemType.DATA_TYPE,
		'void': LexemType.DATA_TYPE
}

lexem_dict = dict(keywords)
lexem_dict.update(types) 
lexem_dict.update(assign) 
lexem_dict.update(operators)
lexem_dict.update(keywords)
lexem_dict.update(separators)

tokens = []
cur = ''
string_const_flag = False
string_const_quote = None


def is_variable(c):
	return c.isdigit() or c.isalpha() or c == '_' or c == ':' 


def close_lexem():
	global cur
	if len(cur) > 0:
		if cur in lexem_dict:
			tokens.append((cur, lexem_dict[cur]))	
		elif cur.isdigit():
			tokens.append((cur, LexemType.NUMBER))
		elif cur[0] in quotes and cur[-1] in quotes:
			tokens.append((cur, LexemType.STRING_CONST))
		else:
			tokens.append((cur, LexemType.VARIABLE))
	cur = ''


def lexer(line):
	global cur
	global tokens
	global string_const_flag
	global string_const_quote

	cur = ''
	tokens = []
	for c in line:
		if string_const_flag:
			cur += c
			if c == string_const_quote:
				close_lexem()
				string_const_flag = False
			continue

		if c.isspace():
			close_lexem()
		elif is_variable(c):
			if len(cur) > 0 and not is_variable(cur[-1]):
				close_lexem()
			cur += c
		elif c in symbols:
			if len(cur) > 0 and not cur[-1] in symbols:
				close_lexem()
			cur += c
		elif c in quotes:
			close_lexem()
			string_const_flag = True
			string_const_quote = c
			cur += c
		else:
			close_lexem()
			cur += c
	
	close_lexem()
	return tokens
