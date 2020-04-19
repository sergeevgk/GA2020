import argparse
from antlr4 import *
from json2jsx import JsxEmitter
from json_jsx.JSONLexer import JSONLexer
from json_jsx.JSONParser import JSONParser


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--input', help='Path to input json file')
    parser.add_argument("-o", '--output', help='Path to output file')
    args = parser.parse_args()
    input_stream = FileStream(args.input)

    lexer = JSONLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = JSONParser(token_stream)
    tree = parser.json()

    lisp_tree_str = tree.toStringTree(recog=parser)

    # listener
    print("Start Walking...")
    listener = JsxEmitter()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    f = open(args.output, "w")
    f.write(listener.getJSX(tree))
    f.close()
