"""
Parser test cases for TyC compiler
TODO: Implement 100 test cases for parser
"""

import pytest
from tests.utils import Parser, Tokenizer


def test_001():
    source = "\t \n\r"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_002():
    source = "/* comment */ // line"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_003():
    source = "@"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Error Token @"


def test_004():
    source = "#"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Error Token #"


# ===================== IDENTIFIER / KEYWORD =====================

def test_005():
    source = "auto auto1"
    expected = "AUTO,auto,ID,auto1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_006():
    source = "int float bool string"
    expected = "INT,int,FLOAT,float,BOOL,bool,STRING,string,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_007():
    source = "_a A1 a_b_c"
    expected = "ID,_a,ID,A1,ID,a_b_c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_008():
    source = "if else for while return break continue"
    expected = (
        "IF,if,ELSE,else,FOR,for,WHILE,while,"
        "RETURN,return,BREAK,break,CONTINUE,continue,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


# ===================== INTEGER =====================

def test_009():
    source = "0 1 10 999"
    expected = (
        "INT_LIT,0,INT_LIT,1,INT_LIT,10,INT_LIT,999,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_010():
    source = "-1 -20"
    expected = (
        "MINUS,-,INT_LIT,1,MINUS,-,INT_LIT,20,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_011():
    source = "000 0123"
    expected = "INT_LIT,000,INT_LIT,0123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


# ===================== FLOAT =====================

def test_012():
    source = "0.0 3.14 2."
    expected = (
        "FLOAT_LIT,0.0,FLOAT_LIT,3.14,FLOAT_LIT,2.,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_013():
    source = ".5 1e2 1.2E-3"
    expected = (
        "FLOAT_LIT,.5,FLOAT_LIT,1e2,FLOAT_LIT,1.2E-3,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


# ===================== STRING =====================

def test_014():
    source = "\"hello\""
    expected = "STRING_LIT,hello,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_015():
    source = "\"hello \\t world\""
    expected = "STRING_LIT,hello \\t world,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_016():
    source = "\"bad \\q\""
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Illegal Escape In String: bad \\q"


def test_017():
    source = "\"unclosed"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Unclosed String: unclosed"


# ===================== OPERATOR =====================

def test_018():
    source = "+ - * / %"
    expected = (
        "PLUS,+,MINUS,-,MUL,*,DIV,/,MOD,%,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_019():
    source = "== != <= >= < >"
    expected = (
        "EQ,==,NEQ,!=,LE,<=,GE,>=,LT,<,GT,>,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_020():
    source = "&& || !"
    expected = "AND,&&,OR,||,NOT,!,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_021():
    source = "++ --"
    expected = "INC,++,DEC,--,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_022():
    source = "="
    expected = "ASSIGN,=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


# ===================== SEPARATOR =====================

def test_023():
    source = "{ } ( ) ; , :"
    expected = (
        "LBRACE,{,RBRACE,},LPAREN,(,RPAREN,),SEMI,;,COMMA,,,COLON,:,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


# ===================== MIX =====================

def test_024():
    source = "int a=10;"
    expected = (
        "INT,int,ID,a,ASSIGN,=,INT_LIT,10,SEMI,;,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_025():
    source = "a+b*c"
    expected = (
        "ID,a,PLUS,+,ID,b,MUL,*,ID,c,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_026():
    source = "foo(1,2)"
    expected = (
        "ID,foo,LPAREN,(,INT_LIT,1,COMMA,,,INT_LIT,2,RPAREN,),EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_027():
    source = "a.b.c"
    expected = (
        "ID,a,DOT,.,ID,b,DOT,.,ID,c,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_028():
    source = "for(i=0;i<10;i++)"
    expected = (
        "FOR,for,LPAREN,(,ID,i,ASSIGN,=,INT_LIT,0,SEMI,;,"
        "ID,i,LT,<,INT_LIT,10,SEMI,;,ID,i,INC,++,RPAREN,),EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


# ===================== COMMENT EDGE =====================

def test_029():
    source = "a/*x*/b"
    expected = "ID,a,ID,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_030():
    source = "a//x\nb"
    expected = "ID,a,ID,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_031():
    source = "   \n\t  "
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_032():
    source = "// comment only"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_033():
    source = "/* block comment */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_034():
    source = "/* block */ // line"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_035():
    source = "a /* cmt */ b"
    expected = "ID,a,ID,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_036():
    source = "/*multi\nline\ncomment*/"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_037():
    source = "// comment\nx"
    expected = "ID,x,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_038():
    source = "x//comment"
    expected = "ID,x,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_039():
    source = "x/*comment*/y"
    expected = "ID,x,ID,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_040():
    source = "\n//a\n//b\n"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


# ===================== REMAINING =====================

def test_041():
    source = "auto autoX"
    expected = "AUTO,auto,ID,autoX,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_042():
    source = "int integer"
    expected = "INT,int,ID,integer,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_043():
    source = "float float1"
    expected = "FLOAT,float,ID,float1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_044():
    source = "_abc abc_123"
    expected = "ID,_abc,ID,abc_123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_045():
    source = "break breaker"
    expected = "BREAK,break,ID,breaker,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_046():
    source = "while while2"
    expected = "WHILE,while,ID,while2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_047():
    source = "return returnValue"
    expected = "RETURN,return,ID,returnValue,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_048():
    source = "struct structure"
    expected = "STRUCT,struct,ID,structure,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_049():
    source = "bool boolean"
    expected = "BOOL,bool,ID,boolean,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_050():
    source = "void avoid"
    expected = "VOID,void,ID,avoid,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_051():
    source = "0 1 22 333"
    expected = (
        "INT_LIT,0,INT_LIT,1,INT_LIT,22,INT_LIT,333,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_052():
    source = "-1 -22"
    expected = (
        "MINUS,-,INT_LIT,1,MINUS,-,INT_LIT,22,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_053():
    source = "01 001"
    expected = "INT_LIT,01,INT_LIT,001,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_054():
    source = "1.0 2.5"
    expected = "FLOAT_LIT,1.0,FLOAT_LIT,2.5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_055():
    source = ".5 1."
    expected = "FLOAT_LIT,.5,FLOAT_LIT,1.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_056():
    source = "1e3 2E-2"
    expected = "FLOAT_LIT,1e3,FLOAT_LIT,2E-2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_057():
    source = "3.14e10"
    expected = "FLOAT_LIT,3.14e10,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_058():
    source = "0.0e0"
    expected = "FLOAT_LIT,0.0e0,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_059():
    source = "9e+1"
    expected = "FLOAT_LIT,9e+1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_060():
    source = "5E"
    expected = "INT_LIT,5,ID,E,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_061():
    source = "\"hello\""
    expected = "STRING_LIT,hello,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_062():
    source = "\"hello world\""
    expected = "STRING_LIT,hello world,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_063():
    source = "\"tab \\t\""
    expected = "STRING_LIT,tab \\t,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_064():
    source = "\"quote \\\" inside\""
    expected = "STRING_LIT,quote \\\" inside,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_065():
    source = "\"\""
    expected = "STRING_LIT,,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_066():
    source = "\"unclosed"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Unclosed String: unclosed"


def test_067():
    source = "\"illegal \\z\""
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Illegal Escape In String: illegal \\z"


def test_068():
    source = "\"line\nbreak\""
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception:
        assert True


def test_069():
    source = "\"\\\\\""
    expected = "STRING_LIT,\\\\,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_070():
    source = "\"a\"\"b\""
    expected = "STRING_LIT,a,STRING_LIT,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_071():
    source = "+"
    expected = "PLUS,+,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_072():
    source = "++"
    expected = "INC,++,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_073():
    source = "+ +"
    expected = "PLUS,+,PLUS,+,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_074():
    source = "= =="
    expected = "ASSIGN,=,EQ,==,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_075():
    source = "!= !"
    expected = "NEQ,!=,NOT,!,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_076():
    source = "&& ||"
    expected = "AND,&&,OR,||,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_077():
    source = "< <= > >="
    expected = "LT,<,LE,<=,GT,>,GE,>=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_078():
    source = "( ) { } ; ,"
    expected = (
        "LPAREN,(,RPAREN,),LBRACE,{,RBRACE,},SEMI,;,COMMA,,,EOF"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_079():
    source = "a+b*c"
    expected = "ID,a,PLUS,+,ID,b,MUL,*,ID,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_080():
    source = "a++--"
    expected = "ID,a,INC,++,DEC,--,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_081():
    source = "@"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Error Token @"


def test_082():
    source = "#"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Error Token #"


def test_083():
    source = "a @ b"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Error Token @"


def test_084():
    source = "$"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Error Token $"


def test_085():
    source = "?"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Error Token ?"


def test_086():
    source = "123abc"
    expected = "INT_LIT,123,ID,abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_087():
    source = "abc123"
    expected = "ID,abc123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_088():
    source = "0x12"
    expected = "INT_LIT,0,ID,x12,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_089():
    source = "1..2"
    expected = "FLOAT_LIT,1.,FLOAT_LIT,.2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_090():
    source = "1e-"
    expected = "INT_LIT,1,ID,e,MINUS,-,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_091():
    source = "a/*c*/+b"
    expected = "ID,a,PLUS,+,ID,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_092():
    source = "\"a\"/*c*/\"b\""
    expected = "STRING_LIT,a,STRING_LIT,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_093():
    source = "//\n@"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Error Token @"


def test_094():
    source = " \n\t@"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Error Token @"


def test_095():
    source = "\"\"\""
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception:
        assert True


def test_096():
    source = "/* unterminated"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception:
        assert True


def test_097():
    source = "\"\\\"\""
    expected = "STRING_LIT,\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_098():
    source = "\"\\\\t\""
    expected = "STRING_LIT,\\\\t,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_099():
    source = "true false"
    expected = "ID,true,ID,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_100():
    source = "EOF"
    expected = "ID,EOF,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected