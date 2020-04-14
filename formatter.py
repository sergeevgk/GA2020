from parser import NodeType, Node


def format(node, depth=-1):
	output = ''
	if node.text:
		output += ' ' * (3 * depth) + node.text

	if node.type != NodeType.ROOT and len(node.children) > 0:
		output += ' {'
	output += '\n'
	for c in node.children:
		output += format(c, depth + 1)

	if node.type != NodeType.ROOT and len(node.children) > 0:
		output += ' ' * (3 * depth) + '}'

	return output
