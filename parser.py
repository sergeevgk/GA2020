from enum import Enum

from lexer import LexemType


class NodeType(Enum):
	ROOT = -1
	DIRECTIVE = 0
	FUNC_DECL = 1
	CODE = 2
	CONDITION = 3 
	UNKNOWN = 4
	CODE_BLOCK = 5


class Node(object):
	def __init__(self, t):
		self.type = t
		self.head = None
		self.args = []
		self.children = []
		self.text = ''
		self.parent = None


stack = []

dir_flag = False
round_bracket_cnt = 0

root = Node(NodeType.ROOT)


def parse(lexems):
	global root
	cur_node = root

	i = 0
	while i < len(lexems):
		l, t = lexems[i]
		if t == LexemType.SHARP:
			node = Node(NodeType.DIRECTIVE)
			l1, t1 = lexems[i + 1]
			l2, t2 = lexems[i + 2]
				
			if t2 == LexemType.STRING_CONST:
				node.text = l + l1 + ' ' + l2
				i += 2
			else:
				l3, t3 = lexems[i + 3]
				l4, t4 = lexems[i + 4]
				node.text = l + l1 + ' ' + l2 + l3 + l4 
				i += 4

			cur_node.children.append(node)
			continue

		if t == LexemType.DATA_TYPE:
			l1, t1 = lexems[i + 1]
			l2, t2 = lexems[i + 2]
			i += 2

			if t2 == LexemType.ROUND_BRACKET_OPEN:
				node = Node(NodeType.FUNC_DECL)
				node.text = l + ' ' + l1 + ' ' + l2
				while t != LexemType.ROUND_BRACKET_CLOSE:
					i += 1
					l, t = lexems[i]
					node.text += ' ' + l
				node.parent = cur_node
				cur_node.children.append(node)
				cur_node = node
			else:
				node = Node(NodeType.CODE)
				node.text = l + ' ' + l1 + ' ' + l2
				while t != LexemType.SEMICOLON:
					i += 1
					l, t = lexems[i]
					node.text += ' ' + l
				cur_node.children.append(node)
		i += 1

	return root
