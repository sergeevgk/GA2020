from abstract_class.absract_class import AbstractClass
from abstract_class.absract_class import AbstractProperty
from abstract_class.absract_class import AbstractAttribute
from typing import List
import logging


class parser:
    cur_line = 0

    @staticmethod
    def _parse_class(lines: List[str]):
        #parse class name
        class_and_name = lines[parser.cur_line].split(' ')
        if len(class_and_name) < 2:
            logging.error(f"syntax error in string: {parser.cur_line}, must be class ClassName, but was {lines[parser.cur_line]}")
            exit(-1)

        abstr_class = AbstractClass(class_and_name[1])
        while parser.cur_line < len(lines):
            a = 2

    @staticmethod
    def _parse_attr(line: str):
        res = AbstractAttribute()
        s1 = line.split('[')
        if len(s1) is not 2:
            logging.error(f"syntax error in line {parser.cur_line}. Expected [Attribute[=val]], but was {line}")
            exit(-1)

        s2 = s1[1].split(']')


        return res

    @staticmethod
    def parse_abstract_class(file_name: str):
        # read file
        file = open(file_name, 'r')
        lines = file.readlines()

        # now we will fill abstract class by lines
        class_attrs: List[AbstractAttribute] = []
        abstr_class: AbstractClass = None

        parser.cur_line = 0
        while parser.cur_line < len(lines):
            line = lines[parser.cur_line]

            if AbstractAttribute.is_attr(line) and abstr_class is None:
                class_attrs.append(AbstractAttribute(line))
            elif AbstractClass.is_class(line):
                abstr_class = parser._parse_class(lines)
                break

            parser.cur_line += 1

        abstr_class.attrs = class_attrs

        return abstr_class
