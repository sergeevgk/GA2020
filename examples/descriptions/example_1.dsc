[json_serializable]
[json_deserializable]
[category=staff]
class Person
{
  bool is_man
  int age
  str first_name
  str last_name

  [const=30]
  int thirty

  [not_serializable]
  bool money_is_not_a_problem

  [not_serializable]
  [static]
  [const=Person]
  str class_name

  [static]
  [const=10]
  int ten

  [static]
  int twelve

  str get_name()
}