grammar JSON;

json:   obj
    |   array
    ;

obj
    :   '{' pair (',' pair)* '}'    # AnObject
    |   '{' '}'                     # EmptyObject
    ;
	
array
    :   '[' value (',' value)* ']'  # ArrayOfValues
    |   '[' ']'                     # EmptyArray
    ;

pair:   STRING ':' value ;

value
    :   STRING		# String
    |   NUMBER		# Atom
    |   obj     	# ObjectValue
    |   array  		# ArrayValue
    |   'true'		# Atom
    |   'false'		# Atom
    |   'null'		# Atom
    ;

LCURLY : '{' ;
LBRACK : '[' ;

// Took from example in internet
STRING :  '"' (ESC | ~["\\])* '"' ;
fragment ESC :   '\\' (["\\/bfnrt] | UNICODE) ;
fragment UNICODE : 'u' HEX HEX HEX HEX ;
fragment HEX : [0-9a-fA-F] ;

NUMBER
    :   '-'? INT '.' INT EXP?
    |   '-'? INT EXP
    |   '-'? INT
    ;
fragment INT :   '0' | '1'..'9' '0'..'9'* ; // no leading zeros
fragment EXP :   [Ee] [+\-]? INT ;

WS  :   [ \t\n\r]+ -> skip ;
