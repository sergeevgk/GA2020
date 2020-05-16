grammar MAPY;

mapy: (newline | func | typedef)* (EOF)? ;  // файл состоит из функций и определений структур
newline: NEWLINE ;

typedef: identifier EQUAL structureType ;  // определение структуры

func: functionСomment* functionDescription functionDeclaration ;  // функция

functionСomment: commentLine newline ;
commentLine: COMMENT_LINE ;  // выражение с комментарием

functionDescription: (functionInput newline)? (functionOutput newline)? ; // "Вход" и "Выход"
functionOutput: FUNCTION_OUTPUT ;
functionInput: FUNCTION_INPUT ;

functionDeclaration: FUNCTION identifier formalParameterList (COLON typeIdentifierList)? suite END FUNCTION ;

identifier: IDENT ;
identifierList: identifier (COMMA identifier)* ;

formalParameterList: LPAREN (parameter (COMMA parameter)*)? RPAREN ;  // перечисление переменных и их типов в виде "arg1 : type1, arg2 : type2"
parameter: identifier COLON typeIdentifier ;
typeIdentifier: typeT | identifier | (CHAR | INTEGER | REAL | STRING) ;  // названия типов переменных
typeIdentifierList: typeIdentifier (COMMA typeIdentifier)* ;  // просто перечесление типов "type1, type2"

suite: simpleStatement | newline statement+ ;  // основной блок выражений, который находится внутри "func", "if", "while" и т.п.
statement: (simpleStatement | structuredStatement) newline ;  // блок выражений

simpleStatement: smallStatement (SEMI smallStatement)* (commentLine)? ;  // перечисление простых выражений в одну строчку с возможностью комментирования в конце строки
smallStatement: assignmentStatement | procedureStatement | flowStatement | selectStatement | swapStatement | arrowStatement | globalStatement | emptyStatement | parameter ;  // простые несоставные выражения

flowStatement: breakStatement | continueStatement | returnStatement | yieldStatement | stopStatement ;  // выражения, которые относятся к потоку выполнения
breakStatement: BREAK ;
continueStatement: CONTINUE ;
returnStatement: RETURN ((parameterList)? | FAIL) ;
yieldStatement: YIELD parameterList ;
stopStatement: STOP ;

selectStatement: SELECT identifier IN variable ; // выражение select

globalStatement: GLOBAL identifierList ; // выражение global

arrowStatement: identifier (LARROW | RARROW) variable ;  // стрелочные выражения для извлечения из/добавления в стек и очередь

swapStatement: variable SWAP variable ;  // выражение swap

emptyStatement: ;  // пустая строка

procedureStatement: functionDesignator;  // вызов функции

assignmentStatement: variable ASSIGN (setExpression | topExpression | expression) ;  // присваивание
variable: identifier (LBRACK parameterList RBRACK | DOT identifier )* ;  // выражение переменной. может быть как обращение к массиву, так и обращение к стрктуре, или и то и другое
expression: orExpression (relationalOperator expression)? ;  // выражение с оператором сравнения
orExpression: xorExpression (orOperator orExpression)? ;  // выражение с оператором "или"
xorExpression: andExpression (xorOperator xorExpression)? ;  // выражение с оператором "исключающее или"
andExpression: additiveExpression (andOperator andExpression)? ;  // выражение с оператором "и"
additiveExpression: multiplicativeExpression (additiveOperator additiveExpression)? ;  // выражение с аддитивным оператором
multiplicativeExpression: signedFactor (multiplicativeOperator multiplicativeExpression)? ;  // выражение с мультипликативным оператором
signedFactor: sign? powerFactor ;  // выражение со знаком
sign: PLUS | MINUS ;
powerFactor: factor (powerOperator powerFactor)? ;  // выражение с оператором "возведение в степень"
powerOperator: POWER ;
multiplicativeOperator: STAR | SLASH | DIV | MOD ;
additiveOperator: PLUS | MINUS ;
andOperator: AND | INTERSECTION | SETMINUS ;
xorOperator: XOR ;
orOperator: OR | UNION ;
relationalOperator: EQUAL | NOT_EQUAL | LT | LE | GE | GT | IN | NOT_IN;
factor: variable | LPAREN expression RPAREN | roundExpression | lengthExpression | functionDesignator | unsignedConstant | setExpression ;  // выражения, к которым могут применяться операторы
roundExpression: LCEIL expression RCEIL | LFLOOR expression RFLOOR | LBRACK expression RBRACK ;  // выражения с округлением
lengthExpression: VSLASH expression VSLASH ;  // выражение для получения мощности
functionDesignator: (identifier | MIN | MAX) LPAREN parameterList? RPAREN ;  // вызов функции. встроены функции "min" и "max"
parameterList: expression (COMMA expression)* ;  // перечисление выражений для вызова функция, обращения к массиву и выражений, связанных с потоком
unsignedConstant: unsignedNumber | char | string ;
unsignedNumber: unsignedInteger | unsignedReal ;
unsignedInteger: NUM_INT ;
unsignedReal: NUM_REAL | INFINITY;
char: CHAR_LITERAL ;
string: STRING_LITERAL | EMPTY_STRING ;
setExpression: (LCURLY elementList RCURLY) | emptySet ;  // определение "множества"
emptySet: EMPTY_SET ;
topExpression: TOP variable ;  // получение верхнего элемента стека

structuredStatement: (ifStatement | repetetiveStatement) (commentLine)? ;  // составные выражения
repetetiveStatement: whileStatement | repeatStatement | forStatement ;  // выражения для повторения одних и тех же операций
whileStatement: WHILE expression DO suite END WHILE;  // while .. do .. end while
repeatStatement: REPEAT suite UNTIL expression ;  // repeat .. until ..
forStatement: FOR (forInStatement | forToStatement) DO suite END FOR ;  // for .. do .. end for
forInStatement: identifier IN variable ;  // x in X
forToStatement: identifier FROM expression (TO | DOWNTO) expression ;  // i from .. to/downto ..
ifStatement: IF expression THEN suite ((newline)? ELSEIF expression THEN suite)* ((newline)? ELSE suite)? END IF ;  // выражение с оператором условия

typeT: subrangeType | arrayType | setType | queueType | stackType ;  // встроенные состовные типы
subrangeType: expression DOTDOT expression ;  // перечисление в виде "начало..конец"
arrayType: ARRAY LBRACK subrangeTypeList RBRACK OF componentType ;  // массив
subrangeTypeList: subrangeType (COMMA subrangeType)* ;  // несколько перечеслений "начало1..конец1, начало2..конец2"
structureType: STRUCT LCURLY structureTypeList RCURLY ;  // структура
structureTypeList: (newline)? parameter ((newline | SEMI) parameter)* ;  // перечисление полей структуры
setType: SET ;
queueType: QUEUE ;
stackType: STACK ;
componentType: typeIdentifier ;
elementList: element (COMMA element)* ;
element: expression (DOTDOT expression)? ;


CHAR: 'char' ;
STRING: 'string' ;
INTEGER: 'integer' | 'int' ;
REAL: 'real' ;

ARRAY: 'array' ;
OF: 'of' ;
SET: 'set' ;
QUEUE: 'queue' ;
STACK: 'stack' ;
STRUCT: 'struct' ;

BREAK: 'break' ;
CONTINUE: 'continue' ;
RETURN: 'return' ;
FAIL: 'fail' ;
YIELD: 'yield' ;
STOP: 'stop' ;

SELECT: 'select' ;
GLOBAL: 'global' ;

MIN: 'min' ;
MAX: 'max' ;
TOP: 'top' ;
VSLASH: '|' ;

FUNCTION: 'func' ;
IF: 'if' ;
THEN: 'then' ;
ELSEIF: 'elseif' ;
ELSE: 'else' ;
FOR: 'for' ;
WHILE: 'while' ;
REPEAT: 'repeat' ;
UNTIL: 'until' ;
DO: 'do' ;
FROM: 'from' ;
TO: 'to' ;
DOWNTO: 'downto' ;
IN: '\\in' ;
END: 'end' ;

LARROW: '\\leftarrow' | '\\gets' ;
RARROW: '\\rightarrow' | '\\to' ;
SWAP: '\\leftrightarrow' ;

INTERSECTION: '\\cap' ;
UNION: '\\cup' ;
SETMINUS: '\\' | '\\setminus' ;

POWER: '^' ;

STAR: '*' ;
SLASH: '/' ;
DIV: 'div' ;
MOD: 'mod' ;

PLUS: '+' ;
MINUS: '-' ;

AND: '&' ;
XOR: '\\^' ;
OR: '\\vee' ;

NOT_IN: '\\notin' ;
EQUAL: '=' ;
NOT_EQUAL: '\\neq' ;
LT: '<' ;
LE: '\\leq' ;
GE: '\\geq' ;
GT: '>' ;

ASSIGN: ':=' ;

COMMA: ',' ;
SEMI: ';' ;
COLON: ':' ;

LPAREN: '(' ;
RPAREN: ')' ;
LBRACK: '[' ;
RBRACK: ']' ;
LCURLY: '{' ;
RCURLY: '}' ;

LFLOOR: '\\lfloor' ;
RFLOOR: '\\rfloor' ;
LCEIL: '\\lceil' ;
RCEIL: '\\rceil' ;

DOT: '.' ;
DOTDOT: '..' ;

IDENT: ('a' .. 'z' | 'A' .. 'Z') ('a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '_')* ;

CHAR_LITERAL: '\'' ~('\'') '\'' ;
STRING_LITERAL: '\'' (~('\''))+ '\'' ;
EMPTY_STRING: '\\varepsilon' ;
EMPTY_SET: '\\varnothing' ;

WS: [ \t] -> skip  ;

NUM_INT: ('0' .. '9')+ ;
NUM_REAL: ('0' .. '9')+ (('.' ('0' .. '9')+ (EXPONENT)?)? | EXPONENT) ;
fragment EXPONENT: ('e') ('+' | '-')? ('0' .. '9')+ ;
INFINITY: '\\infty' ;

NEWLINE: '\r'? '\n' ;

COMMENT_LINE: '//' ~[\r\n]* ;
FUNCTION_INPUT: '\u0412\u0445\u043E\u0434:' ~[\r\n]* ;  // 'Вход:'
FUNCTION_OUTPUT: '\u0412\u044B\u0445\u043E\u0434:' ~[\r\n]* ;  // 'Выход:'
