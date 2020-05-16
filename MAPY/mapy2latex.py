from antlr4 import *
import argparse

from LaTeX_emitter import LaTeXEmitter
from MAPYLexer import MAPYLexer
from MAPYParser import MAPYParser


def register_launch_arguments():
    parser = argparse.ArgumentParser(description='Настройка параметров командной строки', add_help=False)
    parser.add_argument('-h', '--help', help='показать эту подсказку', action='help')
    parser.add_argument('-i', '--input_mapy', help='путь к MAPY файлу для трансляции в LaTeX', required=True)
    parser.add_argument('-o', '--output_latex', help='путь к файлу для сохранение результата трансляции в LaTeX',
                        default='out.tex')

    return parser.parse_args()


def mapy2latex():
    args = register_launch_arguments()

    lexer = MAPYLexer(FileStream(args.input_mapy, 'utf-8'))
    token_stream = CommonTokenStream(lexer)
    parser = MAPYParser(token_stream)
    tree = parser.mapy()

    visitor = LaTeXEmitter()
    visitor.visit(tree)

    with open(args.output_latex, 'w') as f:
        f.write(visitor.latex)


if __name__ == '__main__':
    mapy2latex()
