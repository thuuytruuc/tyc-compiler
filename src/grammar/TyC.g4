grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}
// --- TODO TASK LEXER --- //
// TODO Keywords
AUTO     : 'auto';
BREAK    : 'break';
CASE     : 'case';
CONTINUE : 'continue';
DEFAULT  : 'default';
ELSE     : 'else';
FLOAT    : 'float';
FOR      : 'for';
IF       : 'if';
INT      : 'int';
RETURN   : 'return';
STRING   : 'string';
STRUCT   : 'struct';
SWITCH   : 'switch';
VOID     : 'void';
WHILE    : 'while';
BOOL     : 'bool';

// TODO Operator
PLUS        : '+';
MINUS       : '-';
MUL         : '*';
DIV         : '/';
MOD         : '%';

EQ          : '==';
NEQ         : '!=';
LT          : '<';
GT          : '>';
LE          : '<=';
GE          : '>=';
OR          : '||';
AND         : '&&';
NOT         : '!';
INC         : '++';
DEC         : '--';
ASSIGN      : '=';
DOT         : '.';

// TODO Separator
// LBRACK   : '[';
// RBRACK   : ']';
LBRACE   : '{';
RBRACE   : '}';
LPAREN   : '(';
RPAREN   : ')';
SEMI     : ';';
COMMA    : ',';
COLON    : ':';

// TODO Identifiers
ID : [A-Za-z_][a-zA-Z0-9_]* ;

// TODO Literals
INT_LIT    : [0-9]+ ;
FLOAT_LIT   : [0-9]+ DECIMAL EXPONENT?
            | '.' [0-9]+ EXPONENT?
            | [0-9]+ EXPONENT
            ;
STRING_LIT : '"' STR_CHAR* '"' {self.text = self.text[1:-1]} ;
fragment DECIMAL      : '.' [0-9]* ;
fragment EXPONENT : [eE] [+-]? [0-9]+ ;
fragment ESC_SEQ      : '\\' [bfrnt\\"] ;
fragment ESC_ILLEGAL  : '\\' ~[bfrnt\\"];
fragment STR_CHAR     : ~[\n\\"] | ESC_SEQ ;

// TODO Comment and WS
BLOCK_COMMENT
    :   '/*' .*? '*/' -> skip
    ;
LINE_COMMENT
    :   '//' ~[\r\n]* -> skip
    ;
WS: [ \t\r\n\f]+ -> skip ;

// TODO ERROR
ERROR_CHAR: .;
UNCLOSE_STRING: '"' STR_CHAR*  '\\'? ('\n' | '\r\n' | EOF) {
    if self.text[-1] == '\n' and self.text[-2] == '\r':
        raise UncloseString(self.text[1:-2])
    elif self.text[-1] == '\n':
        raise UncloseString(self.text[1:-1])
    else:
        raise UncloseString(self.text[1:])
};

ILLEGAL_ESCAPE: '"' STR_CHAR* ESC_ILLEGAL {
    raise IllegalEscape(self.text[1:])
};

// --- PARSER --- //
// TODO Expressions
/*
| **Operator** | **Associativity** |
|--------------|-------------------|
| `++`, `--` (postfix) | left |
| `++`, `--` (prefix) | right |
| `!`, `-` (unary), `+` (unary) | right |
| `.` (member access) | left |
| `*`, `/`, `%` | left |
| `+`, `-` (binary) | left |
| `<`, `<=`, `>`, `>=` | left |
| `==`, `!=` | left |
| `&&` | left |
| `\|\|` | left |
| `=` | right |
Primary expressions (identifiers, literals, parenthesized, member access), 
unary operations, binary operations following operator precedence, 
function calls, and postfix operations (increment/decrement)
*/
list_expression: expression COMMA list_expression | expression;
expression  : ((element | INT_LIT | FLOAT_LIT) ASSIGN expression) | expression1 ;
expression1 : expression1 OR expression2 | expression2 ;
expression2 : expression2 AND expression3 | expression3 ;
expression3 : expression3 (EQ | NEQ) expression4 | expression4 ;
expression4 : expression4 (LT | LE | GT | GE) expression5 | expression5 ;
expression5 : expression5 (PLUS | MINUS) expression6 | expression6 ;
expression6 : expression6 (MUL | DIV | MOD) expression7 | expression7 ;
expression7 : (NOT | '-' | '+') expression7 | expression8 ;
expression8 : (INC | DEC) expression8 | expression9 ;
expression9: expression9 (INC | DEC) | expression10 ;
expression10: expression10 DOT ID | expression11 ;
expression11: ID (DOT ID)* | literal | LPAREN expression RPAREN | function_call ;
element: ID (DOT ID)* 
    | lhs (DOT ID)+;
lhs: function_call | LPAREN expression RPAREN | literal | LBRACE list_expression RBRACE;

// TODO type `int`, `float`, `string`, `void`, struct types, and type inference using `auto`
function : (non_auto_type | ID | VOID)? ID LPAREN list_param? RPAREN LBRACE list_statement? RBRACE;
list_param : param COMMA list_param | param ;
param      : (primitive_type | ID) ID ;

function_call: ID LPAREN list_expression? RPAREN ;
 
literal: INT_LIT | FLOAT_LIT | STRING_LIT | struct_literal;

structs: struct_declared structs* | struct_declared;
struct_declared: STRUCT ID LBRACE (struct_mem SEMI)* RBRACE SEMI ;
struct_mem: (primitive_type | ID) ID;
struct_literal: LBRACE list_expression? RBRACE ;

primitive_type : INT | FLOAT | BOOL | STRING ;
non_auto_type : primitive_type | STRUCT ;
all_type : non_auto_type | AUTO | ID;
// TODO Statements Variable declarations, assignments, control flow (if, while, for, switch-case), break, continue, return, expression statements, and blocks
list_statement: statement list_statement | statement;
statement: assign_statement SEMI
        | var_statement SEMI
        | if_statement
        | while_statement
        | for_statement
        | switch_statement
        | break_statement
        | continue_statement
        | block_statement
        | expression_statement SEMI
        | return_statement;
assign_statement: element ASSIGN expression
        | ID ID ASSIGN LBRACE list_expression RBRACE ;
var_statement: (primitive_type | AUTO | ID) ID (ASSIGN expression)? ;
if_statement: IF LPAREN expression RPAREN statement (ELSE if_statement)?
    | IF LPAREN expression RPAREN statement (ELSE statement)?;
while_statement : WHILE LPAREN expression RPAREN (statement | block_statement) ;

for_statement: FOR LPAREN (var_statement | assign_statement)? SEMI 
        expression? SEMI 
        update_statement? RPAREN 
        (statement | block_statement | break_statement) ;
update_statement: assign_statement 
    | (INC|DEC)* update_statement_lhs (INC|DEC)+
    | (INC|DEC)+ update_statement_lhs (INC|DEC)*;
update_statement_lhs: ID (DOT ID)*  | LPAREN expression RPAREN | LBRACE list_expression RBRACE | INT_LIT | FLOAT_LIT;

switch_statement: SWITCH LPAREN expression RPAREN LBRACE switch_block RBRACE;
switch_block: switch_label* default_label? switch_label*;
switch_label: CASE expression COLON list_statement?;
default_label: DEFAULT COLON list_statement?;

break_statement: BREAK SEMI ;
continue_statement: CONTINUE SEMI;
block_statement: (LBRACE list_statement? RBRACE);
expression_statement: expression ;
return_statement: RETURN expression? SEMI;

// TODO Structs and Functions
program: (structs | function)* EOF;