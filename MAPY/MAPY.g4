grammar MAPY;

mapy: (newline | func | typedef)* (EOF)? ;
newline: NEWLINE ;

typedef: identifier EQUAL structureType ;

func: functionСomment* functionDescription functionDeclaration ;

functionСomment: commentLine newline ;
commentLine: COMMENT_LINE ;

functionDescription: (functionInput newline)? (functionOutput newline)? ;
functionOutput: FUNCTION_OUTPUT ;
functionInput: FUNCTION_INPUT ;

functionDeclaration: FUNCTION identifier formalParameterList (COLON typeIdentifierList)? suite END FUNCTION ;

identifier: IDENT ;
identifierList: identifier (COMMA identifier)* ;

formalParameterList: LPAREN (parameter (COMMA parameter)*)? RPAREN ;
parameter: identifier COLON typeIdentifier ;
typeIdentifier: typeT | identifier | (CHAR | INTEGER | REAL | STRING) ;
typeIdentifierList: typeIdentifier (COMMA typeIdentifier)* ;

suite: simpleStatement | newline statement+ ;
statement: (simpleStatement | structuredStatement) newline ;

simpleStatement: smallStatement (SEMI smallStatement)* (commentLine)? ;
smallStatement: assignmentStatement | procedureStatement | flowStatement | selectStatement | swapStatement | arrowStatement | globalStatement | emptyStatement | parameter ;

flowStatement: breakStatement | continueStatement | returnStatement | yieldStatement | stopStatement ;
breakStatement: BREAK ;
continueStatement: CONTINUE ;
returnStatement: RETURN ((parameterList)? | FAIL) ;
yieldStatement: YIELD parameterList ;
stopStatement: STOP ;

selectStatement: SELECT identifier IN variable ;

globalStatement: GLOBAL identifierList ;

arrowStatement: identifier (LARROW | RARROW) variable ;

swapStatement: variable SWAP variable ;

emptyStatement: ;

procedureStatement: functionDesignator;

assignmentStatement: variable ASSIGN (setExpression | topExpression | expression) ;
variable: identifier (LBRACK parameterList RBRACK | DOT identifier )* ;
expression: orExpression (relationalOperator expression)? ;
orExpression: xorExpression (orOperator orExpression)? ;
xorExpression: andExpression (xorOperator xorExpression)? ;
andExpression: additiveExpression (andOperator andExpression)? ;
additiveExpression: multiplicativeExpression (additiveOperator additiveExpression)? ;
multiplicativeExpression: signedFactor (multiplicativeOperator multiplicativeExpression)? ;
signedFactor: sign? powerFactor ;
sign: PLUS | MINUS ;
powerFactor: factor (powerOperator powerFactor)? ;
powerOperator: POWER ;
multiplicativeOperator: STAR | SLASH | DIV | MOD ;
additiveOperator: PLUS | MINUS ;
andOperator: AND | INTERSECTION | SETMINUS ;
xorOperator: XOR ;
orOperator: OR | UNION ;
relationalOperator: EQUAL | NOT_EQUAL | LT | LE | GE | GT | IN | NOT_IN;
factor: variable | LPAREN expression RPAREN | roundExpression | lengthExpression | functionDesignator | unsignedConstant | setExpression ;
roundExpression: LCEIL expression RCEIL | LFLOOR expression RFLOOR | LBRACK expression RBRACK ;
lengthExpression: VSLASH expression VSLASH ;
functionDesignator: (identifier | MIN | MAX) LPAREN parameterList? RPAREN ;
parameterList: expression (COMMA expression)* ;
unsignedConstant: unsignedNumber | char | string ;
unsignedNumber: unsignedInteger | unsignedReal ;
unsignedInteger: NUM_INT ;
unsignedReal: NUM_REAL | INFINITY;
char: CHAR_LITERAL ;
string: STRING_LITERAL | EMPTY_STRING ;
setExpression: (LCURLY elementList RCURLY) | emptySet ;
emptySet: EMPTY_SET ;
topExpression: TOP variable ;

structuredStatement: (ifStatement | repetetiveStatement) (commentLine)? ;
repetetiveStatement: whileStatement | repeatStatement | forStatement ;
whileStatement: WHILE expression DO suite END WHILE;
repeatStatement: REPEAT suite UNTIL expression ;
forStatement: FOR (forInStatement | forToStatement) DO suite END FOR ;
forInStatement: identifier IN variable ;
forToStatement: identifier FROM expression (TO | DOWNTO) expression ;
ifStatement: IF expression THEN suite ((newline)? ELSEIF expression THEN suite)* ((newline)? ELSE suite)? END IF ;

typeT: subrangeType | arrayType | setType | queueType | stackType ;
subrangeType: expression DOTDOT expression ;
arrayType: ARRAY LBRACK subrangeTypeList RBRACK OF componentType ;
subrangeTypeList: subrangeType (COMMA subrangeType)* ;
structureType: STRUCT LCURLY structureTypeList RCURLY ;
structureTypeList: (newline)? parameter ((newline | SEMI) parameter)* ;
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
FUNCTION_INPUT: '\u0412\u0445\u043E\u0434:' ~[\r\n]* ; // 'Вход:'
FUNCTION_OUTPUT: '\u0412\u044B\u0445\u043E\u0434:' ~[\r\n]* ; // 'Выход:'
