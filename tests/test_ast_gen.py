"""
AST Generation test cases for TyC compiler (50 Distinct Cases).
"""

from html import parser

import pytest
from tests.utils import ASTGenerator
from src.utils.nodes import *

# ==========================================
# AST GENERATION EXTRA TESTS (001 - 020)
# ==========================================

def test_ast_001():
    source = "void start() { int counter; }"
    expected = Program([
        FuncDecl(VoidType(), "start", [], BlockStmt([
            VarDecl(IntType(), "counter", None)
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_002():
    source = "void entry() { float temperature; }"
    expected = Program([
        FuncDecl(VoidType(), "entry", [], BlockStmt([
            VarDecl(FloatType(), "temperature", None)
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_003():
    source = "void run() { string name; }"
    expected = Program([
        FuncDecl(VoidType(), "run", [], BlockStmt([
            VarDecl(StringType(), "name", None)
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_004():
    source = "void start() { int a = 5; }"
    expected = Program([
        FuncDecl(VoidType(), "start", [], BlockStmt([
            VarDecl(IntType(), "a", IntLiteral(5))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_005():
    source = "void start() { float pi = 3.0; }"
    expected = Program([
        FuncDecl(VoidType(), "start", [], BlockStmt([
            VarDecl(FloatType(), "pi", FloatLiteral(3.0))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_006():
    source = 'void start() { string msg = "hello"; }'
    expected = Program([
        FuncDecl(VoidType(), "start", [], BlockStmt([
            VarDecl(StringType(), "msg", StringLiteral("hello"))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_007():
    source = "struct Vec { int x; int y; };"
    expected = Program([
        StructDecl("Vec", [
            MemberDecl(IntType(), "x"),
            MemberDecl(IntType(), "y")
        ])
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_008():
    source = "struct Node { int value; Node next; };"
    expected = Program([
        StructDecl("Node", [
            MemberDecl(IntType(), "value"),
            MemberDecl(StructType("Node"), "next")
        ])
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_009():
    source = "int add(int x, int y) {}"
    expected = Program([
        FuncDecl(IntType(), "add", [
            Param(IntType(), "x"),
            Param(IntType(), "y")
        ], BlockStmt([]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_010():
    source = "float area(float r) {}"
    expected = Program([
        FuncDecl(FloatType(), "area", [
            Param(FloatType(), "r")
        ], BlockStmt([]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_011():
    source = "void main() { a + c; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(Identifier("a"), "+", Identifier("c")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_012():
    source = "void main() { m - n; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(Identifier("m"), "-", Identifier("n")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_013():
    source = "void main() { x * y; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(Identifier("x"), "*", Identifier("y")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_014():
    source = "void main() { p / q; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(Identifier("p"), "/", Identifier("q")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_015():
    source = "void main() { -value; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(PrefixOp("-", Identifier("value")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_016():
    source = "void main() { !flag; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(PrefixOp("!", Identifier("flag")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_017():
    source = "void main() { counter++; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(PostfixOp("++", Identifier("counter")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_018():
    source = "void main() { index--; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(PostfixOp("--", Identifier("index")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_019():
    source = "void main() { total = 42; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(
                Identifier("total"),
                IntLiteral(42)
            ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_020():
    source = "void main() { log(); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("log", []))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

# ==========================================
# AST GENERATION EXTRA TESTS (021 - 100)
# ==========================================

def test_ast_021():
    source = "void main(){ a < b; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(Identifier("a"), "<", Identifier("b")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_022():
    source = "void main(){ left > right; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(Identifier("left"), ">", Identifier("right")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_023():
    source = "void main(){ alpha <= beta; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(Identifier("alpha"), "<=", Identifier("beta")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_024():
    source = "void main(){ u >= v; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(Identifier("u"), ">=", Identifier("v")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_025():
    source = "void main(){ a == b; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(Identifier("a"), "==", Identifier("b")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_026():
    source = "void main(){ x != y; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(Identifier("x"), "!=", Identifier("y")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_027():
    source = "void main(){ flagA && flagB; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(Identifier("flagA"), "&&", Identifier("flagB")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_028():
    source = "void main(){ cond1 || cond2; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(Identifier("cond1"), "||", Identifier("cond2")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_029():
    source = "void main(){ value = 7; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("value"), IntLiteral(7)))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_030():
    source = "void main(){ process(5); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("process", [IntLiteral(5)]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_031():
    source = "void main(){ sum(a, b); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("sum", [Identifier("a"), Identifier("b")]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_032():
    source = "void main(){ data.value; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(MemberAccess(Identifier("data"), "value"))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_033():
    source = "void main(){ obj.a.b; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(MemberAccess(MemberAccess(Identifier("obj"), "a"), "b"))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_034():
    source = "void main(){ compute().res; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(MemberAccess(FuncCall("compute", []), "res"))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_035():
    source = "void main(){ if(a){} }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(Identifier("a"), BlockStmt([]), None)
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_036():
    source = "void main(){ if(x){} else{} }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(Identifier("x"), BlockStmt([]), BlockStmt([]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_037():
    source = "void main(){ while(flag){} }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            WhileStmt(Identifier("flag"), BlockStmt([]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_038():
    source = "void main(){ for(;;){} }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(None, None, None, BlockStmt([]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_039():
    source = "void main(){ break; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            BreakStmt()
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_040():
    source = "void main(){ return a; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ReturnStmt(Identifier("a"))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_041():
    source = "void main(){ a = b = 9; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(
                Identifier("a"),
                AssignExpr(Identifier("b"), IntLiteral(9))
            ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_042():
    source = "void main(){ res = -x; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("res"), PrefixOp("-", Identifier("x"))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_043():
    source = "void main(){ y = !flag; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("y"), PrefixOp("!", Identifier("flag"))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_044():
    source = "void main(){ score = a + b * c; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(
                Identifier("score"),
                BinaryOp(
                    Identifier("a"),
                    "+",
                    BinaryOp(Identifier("b"), "*", Identifier("c"))
                )
            ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_045():
    source = "void main(){ print(max(x, y)); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("print", [
                FuncCall("max", [Identifier("x"), Identifier("y")])
            ]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_046():
    source = "void main(){ obj.val = 3; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(
                MemberAccess(Identifier("obj"), "val"),
                IntLiteral(3)
            ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_047():
    source = "void main(){ node.next.data = k; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(
                MemberAccess(MemberAccess(Identifier("node"), "next"), "data"),
                Identifier("k")
            ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_048():
    source = "void main(){ while(i < 5){ i++; } }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            WhileStmt(
                BinaryOp(Identifier("i"), "<", IntLiteral(5)),
                BlockStmt([
                    ExprStmt(PostfixOp("++", Identifier("i")))
                ])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_049():
    source = "void main(){ if(a) b++; else b--; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(
                Identifier("a"),
                ExprStmt(PostfixOp("++", Identifier("b"))),
                ExprStmt(PostfixOp("--", Identifier("b")))
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_050():
    source = "void main(){ return 0; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ReturnStmt(IntLiteral(0))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


# ==========================================
# AST GENERATION EXTRA STRUCTURAL TESTS (051 - 100)
# ==========================================

def test_ast_051():
    source = "void main(){ foo = bar + 1; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("foo"), BinaryOp(Identifier("bar"), "+", IntLiteral(1))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_052():
    source = "void main(){ baz--; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(PostfixOp("--", Identifier("baz")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_053():
    source = "void main(){ -neg; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(PrefixOp("-", Identifier("neg")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_054():
    source = "void main(){ a * b / c; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(BinaryOp(Identifier("a"), "*", Identifier("b")), "/", Identifier("c")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_055():
    source = "void main(){ (x + y) * z; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(BinaryOp(Identifier("x"), "+", Identifier("y")), "*", Identifier("z")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_056():
    source = "void main(){ !done; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(PrefixOp("!", Identifier("done")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_057():
    source = "void main(){ user.profile; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(MemberAccess(Identifier("user"), "profile"))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_058():
    source = "void main(){ arr.length; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(MemberAccess(Identifier("arr"), "length"))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_059():
    source = "void main(){ call(); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("call", []))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_060():
    source = "void main(){ check(1, 2, 3); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("check", [IntLiteral(1), IntLiteral(2), IntLiteral(3)]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_061():
    source = "void main(){ if(valid){} }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(Identifier("valid"), BlockStmt([]), None)
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_062():
    source = "void main(){ if(a){} else{} }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(Identifier("a"), BlockStmt([]), BlockStmt([]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_063():
    source = "void main(){ while(active){ x++; } }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            WhileStmt(Identifier("active"), BlockStmt([
                ExprStmt(PostfixOp("++", Identifier("x")))
            ]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_064():
    source = "void main(){ for(;;) break; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(None, None, None, BreakStmt())
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_065():
    source = "void main(){ continue; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ContinueStmt()
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_066():
    source = "void main(){ return; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ReturnStmt(None)
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_067():
    source = "void main(){ n = m = 0; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("n"), AssignExpr(Identifier("m"), IntLiteral(0))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_068():
    source = "void main(){ z = y * 4; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("z"), BinaryOp(Identifier("y"), "*", IntLiteral(4))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_069():
    source = "void main(){ result = compute(a); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("result"), FuncCall("compute", [Identifier("a")])))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_070():
    source = "void main(){ data.info = 10; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(MemberAccess(Identifier("data"), "info"), IntLiteral(10)))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_071():
    source = "void main(){ if(check) update(); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(Identifier("check"), ExprStmt(FuncCall("update", [])), None)
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_072():
    source = "void main(){ if(a) b++; else c--; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(Identifier("a"), ExprStmt(PostfixOp("++", Identifier("b"))), ExprStmt(PostfixOp("--", Identifier("c"))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_073():
    source = "void main(){ while(count < 10) count++; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            WhileStmt(BinaryOp(Identifier("count"), "<", IntLiteral(10)), ExprStmt(PostfixOp("++", Identifier("count"))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_074():
    source = "void main(){ for(;;){} }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(None, None, None, BlockStmt([]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_075():
    source = "void main(){ a = b + c * d; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("a"), BinaryOp(Identifier("b"), "+", BinaryOp(Identifier("c"), "*", Identifier("d")))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_076():
    source = "void main(){ call1(call2(1)); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("call1", [FuncCall("call2", [IntLiteral(1)])]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_077():
    source = "void main(){ obj1.obj2.obj3; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(MemberAccess(MemberAccess(Identifier("obj1"), "obj2"), "obj3"))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_078():
    source = "void main(){ a && b || c; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(BinaryOp(Identifier("a"), "&&", Identifier("b")), "||", Identifier("c")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_079():
    source = "void main(){ x == y != z; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(BinaryOp(Identifier("x"), "==", Identifier("y")), "!=", Identifier("z")))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_080():
    source = "void main(){ arr.idx = 5; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(MemberAccess(Identifier("arr"), "idx"), IntLiteral(5)))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_081():
    source = "void main(){ if(flag) break; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(Identifier("flag"), BreakStmt(), None)
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_082():
    source = "void main(){ if(flag) continue; else return; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(Identifier("flag"), ContinueStmt(), ReturnStmt(None))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_083():
    source = "void main(){ while(ok) break; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            WhileStmt(Identifier("ok"), BreakStmt())
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_084():
    source = "void main(){ while(1) continue; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            WhileStmt(IntLiteral(1), ContinueStmt())
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_085():
    source = "void main(){ for(;;) return 1; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(None, None, None, ReturnStmt(IntLiteral(1)))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_086():
    source = "void main(){ sum = a + (b * c); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("sum"), BinaryOp(Identifier("a"), "+", BinaryOp(Identifier("b"), "*", Identifier("c")))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_087():
    source = "void main(){ call(x, y + 2); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("call", [Identifier("x"), BinaryOp(Identifier("y"), "+", IntLiteral(2))]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_088():
    source = "void main(){ object.member = func(); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(MemberAccess(Identifier("object"), "member"), FuncCall("func", [])))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_089():
    source = "void main(){ result = !failed; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("result"), PrefixOp("!", Identifier("failed"))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_090():
    source = "void main(){ var1 = var2 - 8; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("var1"), BinaryOp(Identifier("var2"), "-", IntLiteral(8))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_091():
    source = "void main(){ if(x > 0) y = 1; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(BinaryOp(Identifier("x"), ">", IntLiteral(0)), ExprStmt(AssignExpr(Identifier("y"), IntLiteral(1))), None)
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_092():
    source = "void main(){ if(x < 0) y = -1; else y = 0; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(
                BinaryOp(Identifier("x"), "<", IntLiteral(0)),
                ExprStmt(AssignExpr(Identifier("y"), PrefixOp("-", IntLiteral(1)))),
                ExprStmt(AssignExpr(Identifier("y"), IntLiteral(0)))
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_093():
    source = "void main(){ while(num != 0) num--; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            WhileStmt(BinaryOp(Identifier("num"), "!=", IntLiteral(0)), ExprStmt(PostfixOp("--", Identifier("num"))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_094():
    source = "void main(){ for(;;) foo++; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(None, None, None, ExprStmt(PostfixOp("++", Identifier("foo"))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_095():
    source = "void main(){ a = b = c = 2; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("a"), AssignExpr(Identifier("b"), AssignExpr(Identifier("c"), IntLiteral(2)))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_096():
    source = "void main(){ !(!flag); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(PrefixOp("!", PrefixOp("!", Identifier("flag"))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_097():
    source = "void main(){ (a + b) == (c - d); }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(BinaryOp(Identifier("a"), "+", Identifier("b")), "==", BinaryOp(Identifier("c"), "-", Identifier("d"))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_098():
    source = """
    void main() {
        for(;; 1++) {}
    }
    """
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(None, None, PostfixOp("++", IntLiteral(1)), BlockStmt([]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_099():
    source = "void main(){ return result.value; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ReturnStmt(MemberAccess(Identifier("result"), "value"))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_100():
    source = "void main(){ x = y || z && w; }"
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("x"), BinaryOp(Identifier("y"), "||", BinaryOp(Identifier("z"), "&&", Identifier("w")))))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)