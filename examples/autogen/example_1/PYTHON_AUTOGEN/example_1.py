from .attributes._json import json_serializable_class_attribute
from .attributes._category import category_class_attribute


@json_serializable_class_attribute
@category_class_attribute(name='staff')
class Person(object):
    def __init__(self):

        self.__is_man = None
        self.__age = None
        self.__first_name = None
        self.__last_name = None
        self.__money_is_not_a_problem = None

    @property
    def is_man(self):
        return self.__is_man

    @is_man.setter
    def is_man(self, value):
        self.__is_man = value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        self.__age = value

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @property
    def money_is_not_a_problem(self):
        return self.__money_is_not_a_problem

    @money_is_not_a_problem.setter
    def money_is_not_a_problem(self, value):
        self.__money_is_not_a_problem = value

    def get_name(self) -> str:
        pass

