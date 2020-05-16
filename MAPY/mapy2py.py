from antlr4 import *
import argparse

from Python_emitter import PythonEmitter
from MAPYLexer import MAPYLexer
from MAPYParser import MAPYParser


def register_launch_arguments():
    parser = argparse.ArgumentParser(description='Настройка параметров командной строки', add_help=False)
    parser.add_argument('-h', '--help', help='показать эту подсказку', action='help')
    parser.add_argument('-i', '--input_mapy', help='путь к MAPY файлу для трансляции в Python', required=True)
    parser.add_argument('-o', '--output_py', help='путь к файлу для сохранение результата трансляции в Python',
                        default='out.py')

    return parser.parse_args()


def mapy2py():
    args = register_launch_arguments()

    lexer = MAPYLexer(FileStream(args.input_mapy, 'utf-8'))
    token_stream = CommonTokenStream(lexer)
    parser = MAPYParser(token_stream)
    tree = parser.mapy()

    visitor = PythonEmitter()
    visitor.visit(tree)

    with open(args.output_py, 'w') as f:
        f.write(visitor.python)


if __name__ == '__main__':
    mapy2py()
