import random
import string
import sys


def generate_tree(max_depth, max_children):
    tree = []
    node_shapes = 'circle', 'ellipse', 'polygon', 'diamond', 'septagon', 'octagon', 'egg'
    link_styles = 'dotted', 'bold', 'filled'
    colors = 'goldenrod', 'red', 'blue', 'sienna', 'green', 'black'

    def print_t(depth):
        tree.append('(')
        print_n(random.choice(string.ascii_letters))
        if depth < max_depth:
            for i in range(random.randint(0, max_children)):
                tree.append('\n')
                print_l(random.choice(string.digits))
                print_t(depth + 1)
        tree.append(')')

    def print_n(name):
        tree.append('[')
        tree.append(name)
        print_c('shape', random.choice(node_shapes))
        print_c('fontcolor', random.choice(colors))
        tree.append(']')

    def print_l(name):
        tree.append('<')
        tree.append(name)
        print_c('style', random.choice(link_styles))
        print_c('color', random.choice(colors))
        print_c('fontcolor', random.choice(colors))
        tree.append('>')

    def print_c(atr_name, atr_val):
        tree.append('{')
        tree.append(atr_name)
        tree.append('=')
        tree.append(atr_val)
        tree.append('}')

    print_t(1)
    return ''.join(tree)


filename = "random_generated_tree.txt"
if len(sys.argv) > 1:
    filename  = sys.argv[1]
file = open(filename, 'w')
file.write(generate_tree(6, 3))
file.close()
