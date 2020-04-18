from .attributes.json_attr import json_serializable_class_attribute
from .attributes.json_attr import json_deserializable_class_attribute
from .attributes.category_attr import category_class_attribute
from .abstract_class.abstract_class import AbstractPersonClass


@json_serializable_class_attribute
@json_deserializable_class_attribute
@category_class_attribute(name='staff')
class Person(object):

    __class_name = "Person"
    __ten = 10
    __twelve = None

    def __init__(self):
        self.__abstract_class = AbstractPersonClass()

        self.__is_man = None
        self.__age = None
        self.__first_name = None
        self.__last_name = None
        self.__thirty = 30
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
    def thirty(self):
        return self.__thirty

    @property
    def money_is_not_a_problem(self):
        return self.__money_is_not_a_problem

    @money_is_not_a_problem.setter
    def money_is_not_a_problem(self, value):
        self.__money_is_not_a_problem = value

    @property
    def class_name(self):
        return type(self).__class_name

    @property
    def ten(self):
        return type(self).__ten

    @property
    def twelve(self):
        return type(self).__twelve

    @twelve.setter
    def twelve(self, value):
        type(self).__twelve = value

    @property
    def _abstract_class(self) -> AbstractPersonClass:
        return self.__abstract_class

    def get_name(self) -> str:
        pass

