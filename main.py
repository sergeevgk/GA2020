import os
import sys
import logging
from parser.parser import parser

if __name__ == '__main__':

    if len(sys.argv) < 2:
        logging.error("Program input is: path_to_class_file language1 language2 language[N] "
                      "where language[i] is language for which you want to get class implementation")
        exit(-1)

    file_path = sys.argv[1]

    abstract_class = parser.parse_abstract_class(file_path)

    for i in range(2, len(sys.argv)):
        if sys.argv[i] is 'kotlin':
            pass

    logging.info("successfully created class into {dir}")

