grammar ASTgrammar;
t : '(' SPACE? n SPACE? (l SPACE? t SPACE?)* ')';
n : '[' SPACE? txt SPACE? (c SPACE?)* ']';
l : '<' SPACE? txt SPACE? (c SPACE?)* '>';
c : '{' SPACE? txt SPACE? '}';
txt : SYMBOL (SPACE? SYMBOL)*;
SPACE : [ \t\r\n]+;
SYMBOL: ~( '(' | ')' | '[' | ']' | '<' | '>' | '{' | '}' );
