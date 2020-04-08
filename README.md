# GA2020
# Постановка задачи  
Реализовать язык описания классов, с возможностью задания различных аттрибутов.  

# План работы  
* Конструирование синтаксиса языка - @Ppasha9
* Метамодель языка - @DmitriiTunikov
* Диаграмма использования - @DmitriiTunikov & @Ppasha9 
* Построение абстрактой модели класса по входному файлу - AST.
  * Распарсить входной файл в массив выражений - @DmitriiTunikov
  * Построить AST - @DmitriiTunikov  
* Генерация кода по построенному AST для разных языков программирования(Python, Java) - @Ppasha9

# Пример описания класса на нашем языке
```python
[json_serializable]
[name=first_name + " " + last_name]
[category="staff"]
class Person
{
  bool is_man;
  int age;
  str first_name;
  str last_name;

  [default="True"]
  bool money_is_not_a_problem;
}
```
