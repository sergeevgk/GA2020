# Easy-Pattern-Constructor
IntelliJ IDEA Plugin to simplify design pattern usage. Using DSL method.

## Постановка задачи
Пользователь (программист на java) устанавливает плагин. В процессе разработки он сможет быстро создать шаблон проектирования, а затем дополнить его для своей задачи. 

*Шаблоном проектирования* будем называть подмножество *design patterns* и *idioms* (терминология согласно [UML3](https://uml3.ru/library/design_patterns/design_patterns.html))

Пользователь может:
- выбрать шаблон проектирования
- [выбрать параметры шаблона проектирования] 

Список поддерживаемых паттернов:
- Singleton
- Builder
- Visitor

## Диаграмма использования
![](https://github.com/sergeevgk/GA2020/blob/E-%3D-pc/diagrams/uml_use_case.JPG)

## Описание GUI пользователя

Пример:

1. Нажать ПКМ
2. Выбрать паттерн из выпадающего списка
3. [Выбрать параметры паттерна]
4. Получить сгенерированный код, дополнить его в своих целях

## Диаграмма состояний
![](https://github.com/sergeevgk/GA2020/blob/E-%3D-pc/diagrams/uml_state.jpg)

## Примеры

### Singleton
![](https://github.com/sergeevgk/GA2020/blob/E-%3D-pc/gifs/singleton.gif)

### Builder
![](https://github.com/sergeevgk/GA2020/blob/E-%3D-pc/gifs/builder.gif)

### Visitor
![](https://github.com/sergeevgk/GA2020/blob/E-%3D-pc/gifs/visitor.gif)

