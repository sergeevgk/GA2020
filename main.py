import argparse

from lexer import lexer
from parser import parse
from formatter import format


def parse_arguments():
	arguments_parser = argparse.ArgumentParser('')
	arguments_parser.add_argument('--input_file', default=None, help='path to the input file')
	arguments_parser.add_argument('--output_file', default=None, help='path to the output file')
	arguments_parser.add_argument('--config_file', default=None, help='path to the config file')
	return arguments_parser.parse_args()


def load_cpp(file_name):
	tokens = []
	with open(file_name, "r") as file:
		for line in file:
			tokens += lexer(line)
			print(line)
			for t in lexer(line):
				print(t)
			print('_' * 20)

	return tokens 


def __main__():
	args = parse_arguments()
	input_file = args.input_file
	if input_file is None:
		input_file = "test/test1.cpp"
	tokens = load_cpp(input_file)
	root = parse(tokens)
	print(format(root)) 


__main__()
