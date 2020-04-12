import re

from typing import List

from abstract_class.absract_class import AbstractClass
from abstract_class.absract_class import AbstractProperty
from abstract_class.absract_class import AbstractAttribute
from abstract_class.absract_class import AbstractMethod
from abstract_class.absract_class import AbstractMethodParam


class Parser:
    cur_line = 0

    @staticmethod
    def _parse_method(line: str) -> AbstractMethod:
        meth = AbstractMethod()

        res = re.search('\s*\w+\s+', line)
        meth.return_type = res.group(0).strip()

        cur_pos = res.end()
        res = re.search('\w+\s*\(', line[cur_pos:])
        cur_pos += res.end()
        res1 = res.group(0)
        meth.name = res1[:len(res1) - 1].strip()

        res = re.findall('\w+', line[cur_pos:])

        for i in range(0, len(res) - 1, 2):
            meth.params.append(AbstractMethodParam(res[i], res[i + 1]))

        return meth

    @staticmethod
    def _parse_property(line: str) -> AbstractProperty:
        prop_type = re.search('\w+', line)
        val = re.search('\w+', line[prop_type.end():])

        return AbstractProperty(prop_type.group(0), val.group(0) if val is not None else None)

    @staticmethod
    def _parse_class(lines: List[str]) -> AbstractClass:
        res = re.findall('\w+', lines[Parser.cur_line])
        abstr_class = AbstractClass(res[1])

        Parser.cur_line += 1
        cur_attrs: List[AbstractAttribute] = []
        while Parser.cur_line < len(lines):
            cur_line = lines[Parser.cur_line]
            if AbstractAttribute.is_attr(cur_line):
                cur_attrs.append(Parser._parse_attr(cur_line))
            elif AbstractMethod.is_method(cur_line):
                cur_attrs = []
                meth = Parser._parse_method(cur_line)
                abstr_class.methods.append(meth)
            elif AbstractProperty.is_property(cur_line):
                prop = Parser._parse_property(cur_line)
                prop.attrs = cur_attrs
                cur_attrs = []
                abstr_class.properties.append(prop)

            Parser.cur_line += 1

        return abstr_class

    @staticmethod
    def _parse_attr(line: str) -> AbstractAttribute:
        name = re.search('\w+', line)
        val = re.search('\w+', line[name.end():])

        return AbstractAttribute(name.group(0), val.group(0) if val is not None else None)

    @staticmethod
    def parse_abstract_class(file_name: str):
        # read file
        file = open(file_name, 'r')
        lines = file.readlines()

        # now we will fill abstract class by lines
        class_attrs: List[AbstractAttribute] = []
        abstr_class: AbstractClass = None

        Parser.cur_line = 0
        while Parser.cur_line < len(lines):
            line = lines[Parser.cur_line]

            if AbstractAttribute.is_attr(line) and abstr_class is None:
                class_attrs.append(Parser._parse_attr(line))
            elif AbstractClass.is_class(line):
                abstr_class = Parser._parse_class(lines)
                break

            Parser.cur_line += 1

        abstr_class.attrs = class_attrs

        return abstr_class
