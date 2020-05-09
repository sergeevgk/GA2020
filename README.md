# DiagramVirta

## Постановка задачи:
Реализовать программу визуализации диаграмм Вирта. 


## Описание входного формата данных:
Входной язык(EBNF) порождается следующей грамматикой, правила взяты из книги Grune и  Jacobs "Parsing Techniques: A Practical Guide":
```
<syntax>         ::= <rule> | <rule> <syntax>
<rule>           ::= <ws> "<" <rule-name> ">" <ws> <def-sym> <ws> <exp> <line-end>
<def-sym>        ::= "=" | ":=" | "::="
<line-end>       ::= <ws> ";" | <line-end> <line-end>
<exp>            ::= <term> | "(" <ws> <exp> <ws> ")" | "[" <ws> <exp> <ws> "]" | "{" <ws> <exp> <ws> "}" | <exp> <ws> "|" <ws> <exp> | <exp> "*" | <exp> "+" | <exp> "?" | "(*" <ws> <exp> <ws> "*)" | "(?" <ws> <exp> <ws> "?)" | <num> <ws> "*" <ws> <exp> | <exp> <ws> "," <ws> <exp> | <exp> <ws> <exp>
<ws>             ::= " " <ws> | ""
<term>           ::= <literal> | "<" <rule-name> ">"
<literal>        ::= '"' <text1> '"' | "'" <text2> "'"
<text1>          ::= "" | <character1> <text1>
<text2>          ::= "" | <character2> <text2>
<character1>     ::= <character> | "'"
<character2>     ::= <character> | '"'
<character>      ::= <letter> | <digit> | <symbol>
<rule-name>      ::= <letter> | <rule-name> <rule-char>
<rule-char>      ::= <letter> | <digit> | "-"
<letter>         ::= <lower-case> | <upper-case>
<upper-case>     ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
<lower-case>     ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
<num>            ::= <digit-non-zero> | <num> <digit>
<digit>          ::= "0" | <digit-non-zero>
<digit-non-zero> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<symbol>         ::= "|" | " " | "-" | "!" | "#" | "$" | "%" | "&" | "(" | ")" | "*" | "+" | "," | "-" | "." | "/" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "[" | "\" | "]" | "^" | "_" | "`" | "{" | "|" | "}" | "~"

```




## Структура проекта:
 * папка `src` содержит файлы с исходным кодом на Java
 * папка `grammar` содержит пакет `model` и пакет `diagramm`
 * пакет `model` полностью отвечает за разбор правил контекстно-свободной грамматики, состоит из классов:
    *  `BNFToGrammar.java` - класс, отвечающий за парсер грамматики в EBNF форме *(определение типа конструкции и создание соответвующего екземпляра класса)* .
    *  `Grammar.java` - класс, которая описывает модель грамматики.
    *  `Rule.java` - класс, отвечающий за инициализацию и обработку правила свободно-контекстной грамматики.
    *  `Expression.java` - абстрактный класс, описывающий конструкцию выражения.
    *  `Repetition.java` - класс, отвечающий за разбор выражений, которые могут повторяться ноль или более раз.
    *  `Sequence.java` - класс, отвечающий за последовательностей деятельности в зависимости от цели (либо перед в EBNF, либо в диаграмму Вирта)
    *  `Choise.java` - класс, описывающий операцию выбора.
    *  `Literal.java` - класс, описвающий литералы.
    *  `GrammarToBNF.java` - класс, реализующий переход от свободно-контекстной грамматики к EBNF форме
    *  `GrammarToDiagram.java` - класс, реализующий переход из свободно-контекстной грамматики к диаграмме Вирта
* пакет `diagramm` полностью отвечает за создание и отрисовку диаграмм Вирта, состоит  из классов:
    *  `Diagram.java` - отрисовка всей диаграммы и построение основной зависимости и скелета диаграммы.
    *  `Element.java` - класс, отвечающий за програмное представление примитивных эллементов диаграммы.
    *  `Line.java` - отрисовка линий.
    *  `Loop.java` - отрисовка петлей.
    *  `Choice.java` - отрисовка эелементов выбора
    *  `Sequence.java` - отрисовка скелета последовательностей.
    *  `Text.java` - отрисовка текста.
    *  `DiagramToSVG.java` - класс, отвечающий за отрисовку диаграмм (в векторноm представлении).

### Резльтат выполнения программы
Результат работы программы - диаграмма Вирта.

##### При построении диаграмм учитывают следующие правила:
1) Каждый графический элемент, соответствующий терминалу или нетерминалу, имеет по одному входу и выходу, которые изображаются на противоположных сторонах;
2) Каждому правилу соответствует своя графическая диаграмма, на которой терминалы и нетерминалы соединяются посредством дуг;
3) Альтернативы в правилах задаются ветвлением дуг, а итерации - их слиянием;
4) Одна входная дуга слева, задающая начало правила, и одна выходная, задающая его конец (располагается справа);
5) Направления связей отслеживаются движением от начальной дуги в соответствии с плавными изгибами промежуточных дуг и ветвлений.
6) Количество повторений задается отрезком a..b и расположено внутри цикла, обозначающего повторения

| Name   |      Symbol      |  Diagramm |
|----------|:-------------:|-----------|    
| **definition**  |  `=`  | 
|  |  `:=`  | 
| |  `::=`   | 
| **concatenation** |   `'expression1' , 'expression2'`    |   
|  |    `'expression1' 'expression2'`    |   
| **termination** | `;` |
| **alternation** |`'expression1' | 'expression2'` |
| **option** | `  ['expression']` |
| |`'expression'? ` |
| **repetition** | `{'expression'}` |
|  | `'expression'* `|
|  | `'expression'+ ` |
|  | `N * 'expression' ` |
|  | ` N * ['expression'] ` |
|  | ` N * 'expression'? ` |
| **grouping** | `('expression1' 'expression2')` |
| **literal** |`'expression'`|
|  | `"expression"`|
| **special characters** | `(?all visible characters?)` |
| **comments** | `(*comment*)` |

##### Авторы:
*  *Лавриченко Ольга* - разработчик, студентка СПб ПУ
*  *Павел Кононов* - разработчик, студент СПб ПУ
*  *Дунаева Ольга* - разработчик, студентка СПб ПУ

`Дата: 12/05/20`
`Статус: в процессе`
