"""
Test cases for TyC code generation.
"""

from src.utils.nodes import *
from tests.utils import CodeGenerator


def test_001():
    """Test 1: Hello World - print string"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("Hello World")]))
            ])
        )
    ])
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_002():
    """Test 2: Print integer"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [IntLiteral(42)]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_003():
    """Test 3: Print float"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printFloat", [FloatLiteral(3.14)]))
            ])
        )
    ])
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_004():
    """Test 4: Variable declaration and assignment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_005():
    """Test 5: Binary operation - addition"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(IntLiteral(5), "+", IntLiteral(3))
                ]))
            ])
        )
    ])
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_006():
    """Test 6: Binary operation - multiplication"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(IntLiteral(6), "*", IntLiteral(7))
                ]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_007():
    """Test 7: If statement"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(1), "<", IntLiteral(2)),
                    ExprStmt(FuncCall("printString", [StringLiteral("yes")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("no")]))
                )
            ])
        )
    ])
    expected = "yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_008():
    """Test 8: While loop"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(AssignExpr(
                            Identifier("i"),
                            BinaryOp(Identifier("i"), "+", IntLiteral(1))
                        ))
                    ])
                )
            ])
        )
    ])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_009():
    """Test 9: Function call with return value"""
    ast = Program([
        FuncDecl(
            IntType(),
            "add",
            [Param(IntType(), "a"), Param(IntType(), "b")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    FuncCall("add", [IntLiteral(20), IntLiteral(22)])
                ]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_010():
    """Test 10: Multiple statements - arithmetic operations"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                VarDecl(IntType(), "y", IntLiteral(20)),
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(Identifier("x"), "+", Identifier("y"))
                ]))
            ])
        )
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_011():
    """Test 11: For loop"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ForStmt(
            VarDecl(IntType(), "i", IntLiteral(0)),
            BinaryOp(Identifier("i"), "<", IntLiteral(3)),
            PostfixOp("++", Identifier("i")),
            ExprStmt(FuncCall("printInt", [Identifier("i")]))
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "012"


def test_012():
    """Test 12: Subtraction"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(10), "-", IntLiteral(3))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "7"


def test_013():
    """Test 13: Division"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(20), "/", IntLiteral(4))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "5"


def test_014():
    """Test 14: Modulo"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(17), "%", IntLiteral(5))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "2"


def test_015():
    """Test 15: Float addition"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printFloat", [BinaryOp(FloatLiteral(1.5), "+", FloatLiteral(2.5))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "4.0"


def test_016():
    """Test 16: Float multiplication"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printFloat", [BinaryOp(FloatLiteral(2.0), "*", FloatLiteral(3.0))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "6.0"


def test_017():
    """Test 17: Prefix increment"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(5)),
        ExprStmt(PrefixOp("++", Identifier("x"))),
        ExprStmt(FuncCall("printInt", [Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "6"


def test_018():
    """Test 18: Postfix decrement"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(5)),
        ExprStmt(PostfixOp("--", Identifier("x"))),
        ExprStmt(FuncCall("printInt", [Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "4"


def test_019():
    """Test 19: Prefix decrement"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(10)),
        ExprStmt(PrefixOp("--", Identifier("x"))),
        ExprStmt(FuncCall("printInt", [Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "9"


def test_020():
    """Test 20: Logical NOT - false"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [PrefixOp("!", IntLiteral(1))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "0"


def test_021():
    """Test 21: Logical NOT - true"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [PrefixOp("!", IntLiteral(0))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"


def test_022():
    """Test 22: Logical AND - both true"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(1), "&&", IntLiteral(1))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"


def test_023():
    """Test 23: Logical AND - one false"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(1), "&&", IntLiteral(0))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "0"


def test_024():
    """Test 24: Logical OR - both false"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(0), "||", IntLiteral(0))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "0"


def test_025():
    """Test 25: Logical OR - one true"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(0), "||", IntLiteral(1))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"


def test_026():
    """Test 26: Relational == true"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(5), "==", IntLiteral(5))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"


def test_027():
    """Test 27: Relational != true"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(3), "!=", IntLiteral(7))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"


def test_028():
    """Test 28: Relational >= true"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(5), ">=", IntLiteral(5))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"


def test_029():
    """Test 29: Relational <= true"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(3), "<=", IntLiteral(5))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"


def test_030():
    """Test 30: Relational > false"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(3), ">", IntLiteral(5))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "0"


def test_031():
    """Test 31: Nested if-else"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(5)),
        IfStmt(
            BinaryOp(Identifier("x"), ">", IntLiteral(10)),
            ExprStmt(FuncCall("printString", [StringLiteral("big")])),
            IfStmt(
                BinaryOp(Identifier("x"), ">", IntLiteral(3)),
                ExprStmt(FuncCall("printString", [StringLiteral("mid")])),
                ExprStmt(FuncCall("printString", [StringLiteral("small")]))
            )
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "mid"


def test_032():
    """Test 32: While with break"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "i", IntLiteral(0)),
        WhileStmt(IntLiteral(1), BlockStmt([
            IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(3)), BreakStmt(), None),
            ExprStmt(FuncCall("printInt", [Identifier("i")])),
            ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "012"


def test_033():
    """Test 33: For loop sum"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "s", IntLiteral(0)),
        ForStmt(
            VarDecl(IntType(), "i", IntLiteral(1)),
            BinaryOp(Identifier("i"), "<=", IntLiteral(5)),
            PostfixOp("++", Identifier("i")),
            ExprStmt(AssignExpr(Identifier("s"), BinaryOp(Identifier("s"), "+", Identifier("i"))))
        ),
        ExprStmt(FuncCall("printInt", [Identifier("s")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "15"


def test_034():
    """Test 34: String variable"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(StringType(), "msg", StringLiteral("hello")),
        ExprStmt(FuncCall("printString", [Identifier("msg")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "hello"


def test_035():
    """Test 35: Multiple print calls"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [IntLiteral(1)])),
        ExprStmt(FuncCall("printInt", [IntLiteral(2)])),
        ExprStmt(FuncCall("printInt", [IntLiteral(3)]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "123"


def test_036():
    """Test 36: Recursive factorial"""
    ast = Program([
        FuncDecl(IntType(), "fact", [Param(IntType(), "n")], BlockStmt([
            IfStmt(
                BinaryOp(Identifier("n"), "<=", IntLiteral(1)),
                ReturnStmt(IntLiteral(1)),
                ReturnStmt(BinaryOp(Identifier("n"), "*", FuncCall("fact", [BinaryOp(Identifier("n"), "-", IntLiteral(1))])))
            )
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("fact", [IntLiteral(5)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "120"


def test_037():
    """Test 37: Unary minus"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [PrefixOp("-", IntLiteral(7))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "-7"


def test_038():
    """Test 38: Unary plus"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [PrefixOp("+", IntLiteral(7))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "7"


def test_039():
    """Test 39: Float subtraction"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printFloat", [BinaryOp(FloatLiteral(5.0), "-", FloatLiteral(2.5))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "2.5"


def test_040():
    """Test 40: Float division"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printFloat", [BinaryOp(FloatLiteral(7.5), "/", FloatLiteral(2.5))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "3.0"


def test_041():
    """Test 41: Int and float mixed addition"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printFloat", [BinaryOp(IntLiteral(1), "+", FloatLiteral(2.5))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "3.5"


def test_042():
    """Test 42: Variable assignment update"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(1)),
        ExprStmt(AssignExpr(Identifier("x"), IntLiteral(99))),
        ExprStmt(FuncCall("printInt", [Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "99"


def test_043():
    """Test 43: For loop with continue"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ForStmt(
            VarDecl(IntType(), "i", IntLiteral(0)),
            BinaryOp(Identifier("i"), "<", IntLiteral(5)),
            PostfixOp("++", Identifier("i")),
            BlockStmt([
                IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(2)), ContinueStmt(), None),
                ExprStmt(FuncCall("printInt", [Identifier("i")]))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "0134"


def test_044():
    """Test 44: Nested function calls"""
    ast = Program([
        FuncDecl(IntType(), "double", [Param(IntType(), "n")], BlockStmt([
            ReturnStmt(BinaryOp(Identifier("n"), "*", IntLiteral(2)))
        ])),
        FuncDecl(IntType(), "quadruple", [Param(IntType(), "n")], BlockStmt([
            ReturnStmt(FuncCall("double", [FuncCall("double", [Identifier("n")])]))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("quadruple", [IntLiteral(5)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "20"


def test_045():
    """Test 45: Return from function early"""
    ast = Program([
        FuncDecl(IntType(), "abs_val", [Param(IntType(), "n")], BlockStmt([
            IfStmt(
                BinaryOp(Identifier("n"), "<", IntLiteral(0)),
                ReturnStmt(PrefixOp("-", Identifier("n"))),
                None
            ),
            ReturnStmt(Identifier("n"))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("abs_val", [IntLiteral(-5)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "5"


def test_046():
    """Test 46: Multiple parameters"""
    ast = Program([
        FuncDecl(IntType(), "max2", [Param(IntType(), "a"), Param(IntType(), "b")], BlockStmt([
            IfStmt(
                BinaryOp(Identifier("a"), ">", Identifier("b")),
                ReturnStmt(Identifier("a")),
                ReturnStmt(Identifier("b"))
            )
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("max2", [IntLiteral(7), IntLiteral(3)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "7"


def test_047():
    """Test 47: Accumulate in while"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "n", IntLiteral(10)),
        VarDecl(IntType(), "s", IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("n"), ">", IntLiteral(0)), BlockStmt([
            ExprStmt(AssignExpr(Identifier("s"), BinaryOp(Identifier("s"), "+", Identifier("n")))),
            ExprStmt(PrefixOp("--", Identifier("n")))
        ])),
        ExprStmt(FuncCall("printInt", [Identifier("s")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "55"


def test_048():
    """Test 48: Empty for loop body"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "i", IntLiteral(0)),
        ForStmt(None, BinaryOp(Identifier("i"), "<", IntLiteral(3)), PostfixOp("++", Identifier("i")), BlockStmt([])),
        ExprStmt(FuncCall("printInt", [Identifier("i")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "3"


def test_049():
    """Test 49: Float variable"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(FloatType(), "f", FloatLiteral(3.14)),
        ExprStmt(FuncCall("printFloat", [Identifier("f")]))
    ]))])
    result = CodeGenerator().generate_and_run(ast)
    assert "3.14" in result


def test_050():
    """Test 50: Three functions"""
    ast = Program([
        FuncDecl(IntType(), "a", [], BlockStmt([ReturnStmt(IntLiteral(1))])),
        FuncDecl(IntType(), "b", [], BlockStmt([ReturnStmt(IntLiteral(2))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [BinaryOp(FuncCall("a", []), "+", FuncCall("b", []))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "3"


def test_051():
    """Test 51: Switch with break"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(2)),
        SwitchStmt(Identifier("x"), [
            CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printString", [StringLiteral("one")])), BreakStmt()]),
            CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printString", [StringLiteral("two")])), BreakStmt()]),
            CaseStmt(IntLiteral(3), [ExprStmt(FuncCall("printString", [StringLiteral("three")])), BreakStmt()])
        ], None)
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "two"


def test_052():
    """Test 52: Switch default"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(99)),
        SwitchStmt(Identifier("x"), [
            CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printString", [StringLiteral("one")])), BreakStmt()])
        ], DefaultStmt([ExprStmt(FuncCall("printString", [StringLiteral("other")]))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "other"


def test_053():
    """Test 53: Postfix ++ return original"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(5)),
        ExprStmt(FuncCall("printInt", [PostfixOp("++", Identifier("x"))])),
        ExprStmt(FuncCall("printInt", [Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "56"


def test_054():
    """Test 54: Complex expression"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [
            BinaryOp(
                BinaryOp(IntLiteral(2), "+", IntLiteral(3)),
                "*",
                BinaryOp(IntLiteral(4), "-", IntLiteral(1))
            )
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "15"


def test_055():
    """Test 55: Large integer constant"""
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(FuncCall("printInt", [IntLiteral(1000)]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1000"


def test_056():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [IntLiteral(-42)]))]))])
    assert CodeGenerator().generate_and_run(ast) == "-42"

def test_057():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(0)),
        IfStmt(Identifier("x"), ExprStmt(FuncCall("printString", [StringLiteral("nonzero")])), ExprStmt(FuncCall("printString", [StringLiteral("zero")])))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "zero"

def test_058():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "i", IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"), "<", IntLiteral(2)), BlockStmt([
            VarDecl(IntType(), "j", IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("j"), "<", IntLiteral(2)), BlockStmt([ExprStmt(FuncCall("printInt", [Identifier("j")])), ExprStmt(PrefixOp("++", Identifier("j")))])),
            ExprStmt(PrefixOp("++", Identifier("i")))
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "0101"

def test_059():
    ast = Program([
        FuncDecl(IntType(), "fib", [Param(IntType(), "n")], BlockStmt([
            IfStmt(BinaryOp(Identifier("n"), "<=", IntLiteral(1)), ReturnStmt(Identifier("n")), None),
            ReturnStmt(BinaryOp(FuncCall("fib", [BinaryOp(Identifier("n"), "-", IntLiteral(1))]), "+", FuncCall("fib", [BinaryOp(Identifier("n"), "-", IntLiteral(2))])))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [FuncCall("fib", [IntLiteral(7)])]))]))])
    assert CodeGenerator().generate_and_run(ast) == "13"

def test_060():
    ast = Program([
        FuncDecl(IntType(), "pw", [Param(IntType(), "b"), Param(IntType(), "e")], BlockStmt([
            VarDecl(IntType(), "r", IntLiteral(1)),
            ForStmt(VarDecl(IntType(), "i", IntLiteral(0)), BinaryOp(Identifier("i"), "<", Identifier("e")), PostfixOp("++", Identifier("i")), ExprStmt(AssignExpr(Identifier("r"), BinaryOp(Identifier("r"), "*", Identifier("b"))))),
            ReturnStmt(Identifier("r"))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [FuncCall("pw", [IntLiteral(2), IntLiteral(8)])]))]))])
    assert CodeGenerator().generate_and_run(ast) == "256"

def test_061():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "n", IntLiteral(5)),
        WhileStmt(BinaryOp(Identifier("n"), ">", IntLiteral(0)), BlockStmt([ExprStmt(FuncCall("printInt", [Identifier("n")])), ExprStmt(PrefixOp("--", Identifier("n")))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "54321"

def test_062():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "a", IntLiteral(2)), VarDecl(IntType(), "b", IntLiteral(3)), VarDecl(IntType(), "c", IntLiteral(4)),
        ExprStmt(FuncCall("printInt", [BinaryOp(BinaryOp(Identifier("a"), "*", Identifier("b")), "+", Identifier("c"))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "10"

def test_063():
    ast = Program([
        FuncDecl(IntType(), "gcd", [Param(IntType(), "a"), Param(IntType(), "b")], BlockStmt([
            WhileStmt(BinaryOp(Identifier("b"), "!=", IntLiteral(0)), BlockStmt([
                VarDecl(IntType(), "t", BinaryOp(Identifier("a"), "%", Identifier("b"))),
                ExprStmt(AssignExpr(Identifier("a"), Identifier("b"))),
                ExprStmt(AssignExpr(Identifier("b"), Identifier("t")))
            ])),
            ReturnStmt(Identifier("a"))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [FuncCall("gcd", [IntLiteral(48), IntLiteral(18)])]))]))])
    assert CodeGenerator().generate_and_run(ast) == "6"

def test_064():
    ast = Program([
        FuncDecl(IntType(), "mn", [Param(IntType(), "a"), Param(IntType(), "b")], BlockStmt([IfStmt(BinaryOp(Identifier("a"), "<", Identifier("b")), ReturnStmt(Identifier("a")), ReturnStmt(Identifier("b")))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [FuncCall("mn", [IntLiteral(4), IntLiteral(9)])]))]))])
    assert CodeGenerator().generate_and_run(ast) == "4"

def test_065():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "i", IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"), "<", IntLiteral(6)), BlockStmt([
            ExprStmt(PrefixOp("++", Identifier("i"))),
            IfStmt(BinaryOp(BinaryOp(Identifier("i"), "%", IntLiteral(2)), "==", IntLiteral(0)), ContinueStmt(), None),
            ExprStmt(FuncCall("printInt", [Identifier("i")]))
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "135"

def test_066():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(1)),
        BlockStmt([VarDecl(IntType(), "y", IntLiteral(2)), ExprStmt(FuncCall("printInt", [BinaryOp(Identifier("x"), "+", Identifier("y"))]))])
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "3"

def test_067():
    ast = Program([
        FuncDecl(VoidType(), "greet", [Param(StringType(), "name")], BlockStmt([ExprStmt(FuncCall("printString", [StringLiteral("Hello ")])), ExprStmt(FuncCall("printString", [Identifier("name")]))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("greet", [StringLiteral("World")]))]))])
    assert CodeGenerator().generate_and_run(ast) == "Hello World"

def test_068():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(FloatType(), "s", FloatLiteral(0.0)),
        ForStmt(VarDecl(IntType(), "i", IntLiteral(1)), BinaryOp(Identifier("i"), "<=", IntLiteral(4)), PostfixOp("++", Identifier("i")), ExprStmt(AssignExpr(Identifier("s"), BinaryOp(Identifier("s"), "+", FloatLiteral(1.0))))),
        ExprStmt(FuncCall("printFloat", [Identifier("s")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "4.0"

def test_069():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(0)), VarDecl(IntType(), "y", IntLiteral(5)),
        WhileStmt(BinaryOp(BinaryOp(Identifier("x"), "<", IntLiteral(3)), "&&", BinaryOp(Identifier("y"), ">", IntLiteral(0))), BlockStmt([ExprStmt(PrefixOp("++", Identifier("x"))), ExprStmt(PrefixOp("--", Identifier("y")))])),
        ExprStmt(FuncCall("printInt", [Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "3"

def test_070():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([VarDecl(IntType(), "x", IntLiteral(4)), ExprStmt(FuncCall("printInt", [PrefixOp("++", Identifier("x"))]))]))])
    assert CodeGenerator().generate_and_run(ast) == "5"

def test_071():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "i", IntLiteral(0)),
        ForStmt(None, BinaryOp(Identifier("i"), "<", IntLiteral(3)), None, BlockStmt([ExprStmt(FuncCall("printInt", [Identifier("i")])), ExprStmt(PrefixOp("++", Identifier("i")))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "012"

def test_072():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "s", IntLiteral(0)),
        ForStmt(VarDecl(IntType(), "i", IntLiteral(1)), BinaryOp(Identifier("i"), "<=", IntLiteral(100)), PostfixOp("++", Identifier("i")), ExprStmt(AssignExpr(Identifier("s"), BinaryOp(Identifier("s"), "+", Identifier("i"))))),
        ExprStmt(FuncCall("printInt", [Identifier("s")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "5050"

def test_073():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(1)),
        SwitchStmt(Identifier("x"), [
            CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printString", [StringLiteral("a")]))]),
            CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printString", [StringLiteral("b")])), BreakStmt()])
        ], None)
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "ab"

def test_074():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([VarDecl(IntType(), "x", None), ExprStmt(AssignExpr(Identifier("x"), IntLiteral(77))), ExprStmt(FuncCall("printInt", [Identifier("x")]))]))])
    assert CodeGenerator().generate_and_run(ast) == "77"

def test_075():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printFloat", [PrefixOp("-", FloatLiteral(1.5))]))]))])
    assert CodeGenerator().generate_and_run(ast) == "-1.5"

def test_076():
    ast = Program([
        FuncDecl(StringType(), "sign", [Param(IntType(), "n")], BlockStmt([
            IfStmt(BinaryOp(Identifier("n"), ">", IntLiteral(0)), ReturnStmt(StringLiteral("pos")), None),
            IfStmt(BinaryOp(Identifier("n"), "<", IntLiteral(0)), ReturnStmt(StringLiteral("neg")), None),
            ReturnStmt(StringLiteral("zero"))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printString", [FuncCall("sign", [IntLiteral(-3)])])),
            ExprStmt(FuncCall("printString", [FuncCall("sign", [IntLiteral(0)])])),
            ExprStmt(FuncCall("printString", [FuncCall("sign", [IntLiteral(5)])]))
        ]))])
    assert CodeGenerator().generate_and_run(ast) == "negzeropos"

def test_077():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", None),
        VarDecl(IntType(), "y", AssignExpr(Identifier("x"), IntLiteral(10))),
        ExprStmt(FuncCall("printInt", [Identifier("y")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "10"

def test_078():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        ForStmt(VarDecl(IntType(), "i", IntLiteral(1)), BinaryOp(Identifier("i"), "<=", IntLiteral(6)), PostfixOp("++", Identifier("i")),
            IfStmt(BinaryOp(BinaryOp(Identifier("i"), "%", IntLiteral(3)), "==", IntLiteral(0)), ExprStmt(FuncCall("printString", [StringLiteral("F")])), ExprStmt(FuncCall("printInt", [Identifier("i")]))))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "12F45F"

def test_079():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printString", [StringLiteral("foo")])), ExprStmt(FuncCall("printString", [StringLiteral("bar")])), ExprStmt(FuncCall("printString", [StringLiteral("baz")]))]))])
    assert CodeGenerator().generate_and_run(ast) == "foobarbaz"

def test_080():
    ast = Program([
        FuncDecl(IntType(), "inc", [Param(IntType(), "n")], BlockStmt([ReturnStmt(BinaryOp(Identifier("n"), "+", IntLiteral(1)))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [FuncCall("inc", [FuncCall("inc", [FuncCall("inc", [IntLiteral(0)])])])]))]))])
    assert CodeGenerator().generate_and_run(ast) == "3"

def test_081():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([WhileStmt(IntLiteral(0), ExprStmt(FuncCall("printString", [StringLiteral("x")]))), ExprStmt(FuncCall("printString", [StringLiteral("done")]))]))])
    assert CodeGenerator().generate_and_run(ast) == "done"

def test_082():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([IfStmt(IntLiteral(0), ExprStmt(FuncCall("printString", [StringLiteral("no")])), None), ExprStmt(FuncCall("printString", [StringLiteral("ok")]))]))])
    assert CodeGenerator().generate_and_run(ast) == "ok"

def test_083():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [IntLiteral(0)]))]))])
    assert CodeGenerator().generate_and_run(ast) == "0"

def test_084():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [PrefixOp("!", PrefixOp("!", IntLiteral(1)))]))]))])
    assert CodeGenerator().generate_and_run(ast) == "1"

def test_085():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([VarDecl(IntType(), "x", IntLiteral(10)), ExprStmt(FuncCall("printInt", [PrefixOp("--", Identifier("x"))]))]))])
    assert CodeGenerator().generate_and_run(ast) == "9"

def test_086():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [BinaryOp(FloatLiteral(1.5), "<", FloatLiteral(2.5))]))]))])
    assert CodeGenerator().generate_and_run(ast) == "1"

def test_087():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "found", IntLiteral(0)),
        ForStmt(VarDecl(IntType(), "i", IntLiteral(0)), BinaryOp(Identifier("i"), "<", IntLiteral(10)), PostfixOp("++", Identifier("i")),
                BlockStmt([IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(5)), BlockStmt([ExprStmt(AssignExpr(Identifier("found"), IntLiteral(1))), BreakStmt()]), None)])),
        ExprStmt(FuncCall("printInt", [Identifier("found")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"

def test_088():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(3)),
        ExprStmt(FuncCall("printInt", [BinaryOp(Identifier("x"), "+", Identifier("x"))])),
        ExprStmt(FuncCall("printInt", [BinaryOp(Identifier("x"), "*", Identifier("x"))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "69"

def test_089():
    ast = Program([
        FuncDecl(IntType(), "add3", [Param(IntType(), "a"), Param(IntType(), "b"), Param(IntType(), "c")], BlockStmt([ReturnStmt(BinaryOp(BinaryOp(Identifier("a"), "+", Identifier("b")), "+", Identifier("c")))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [FuncCall("add3", [IntLiteral(1), IntLiteral(2), IntLiteral(3)])]))]))])
    assert CodeGenerator().generate_and_run(ast) == "6"

def test_090():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(1), "||", IntLiteral(0))]))]))])
    assert CodeGenerator().generate_and_run(ast) == "1"

def test_091():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(0), "&&", IntLiteral(1))]))]))])
    assert CodeGenerator().generate_and_run(ast) == "0"

def test_092():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(5), "-", IntLiteral(5))]))]))])
    assert CodeGenerator().generate_and_run(ast) == "0"

def test_093():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(7), "/", IntLiteral(2))]))]))])
    assert CodeGenerator().generate_and_run(ast) == "3"

def test_094():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printFloat", [FloatLiteral(0.0)]))]))])
    assert CodeGenerator().generate_and_run(ast) == "0.0"

def test_095():
    ast = Program([
        FuncDecl(StringType(), "greet", [], BlockStmt([ReturnStmt(StringLiteral("hi"))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printString", [FuncCall("greet", [])]))]))])
    assert CodeGenerator().generate_and_run(ast) == "hi"

def test_096():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(8)),
        ExprStmt(FuncCall("printInt", [PostfixOp("--", Identifier("x"))])),
        ExprStmt(FuncCall("printInt", [Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "87"

def test_097():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "cnt", IntLiteral(0)),
        ForStmt(VarDecl(IntType(), "i", IntLiteral(0)), BinaryOp(Identifier("i"), "<", IntLiteral(3)), PostfixOp("++", Identifier("i")),
            ForStmt(VarDecl(IntType(), "j", IntLiteral(0)), BinaryOp(Identifier("j"), "<", IntLiteral(3)), PostfixOp("++", Identifier("j")),
                ExprStmt(AssignExpr(Identifier("cnt"), BinaryOp(Identifier("cnt"), "+", IntLiteral(1)))))),
        ExprStmt(FuncCall("printInt", [Identifier("cnt")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "9"

def test_098():
    ast = Program([
        FuncDecl(FloatType(), "half", [Param(FloatType(), "x")], BlockStmt([ReturnStmt(BinaryOp(Identifier("x"), "/", FloatLiteral(2.0)))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([ExprStmt(FuncCall("printFloat", [FuncCall("half", [FloatLiteral(5.0)])]))]))])
    assert CodeGenerator().generate_and_run(ast) == "2.5"

def test_099():
    ast = Program([FuncDecl(VoidType(), "main", [], BlockStmt([
        VarDecl(IntType(), "x", IntLiteral(1)),
        SwitchStmt(Identifier("x"), [CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printInt", [IntLiteral(1)]))]), CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printInt", [IntLiteral(2)]))])],
                   DefaultStmt([ExprStmt(FuncCall("printInt", [IntLiteral(3)]))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "123"

def test_100():
    ast = Program([
        FuncDecl(IntType(), "clamp", [Param(IntType(), "v"), Param(IntType(), "lo"), Param(IntType(), "hi")], BlockStmt([
            IfStmt(BinaryOp(Identifier("v"), "<", Identifier("lo")), ReturnStmt(Identifier("lo")), None),
            IfStmt(BinaryOp(Identifier("v"), ">", Identifier("hi")), ReturnStmt(Identifier("hi")), None),
            ReturnStmt(Identifier("v"))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(VarDecl(IntType(), "i", IntLiteral(0)), BinaryOp(Identifier("i"), "<", IntLiteral(5)), PostfixOp("++", Identifier("i")),
                ExprStmt(FuncCall("printInt", [FuncCall("clamp", [Identifier("i"), IntLiteral(1), IntLiteral(3)])])))
        ]))])
    assert CodeGenerator().generate_and_run(ast) == "11233"

def test_101():
    source = """
    void main() {
        int x = 3;
        {
            int x = 2;
        }
        printInt(x);
    }
    """
    from tests.utils import ASTGenerator, CodeGenerator
    ast = ASTGenerator(source).generate()
    assert CodeGenerator().generate_and_run(ast) == "3"

def test_102():
    source = """
    struct Point {
        int x;
        float y;
        string z ;
    };
    void main(){
        Point p = {1,2.2,"votien"};
        printInt(p.x);
        printFloat(p.y);
        printString(p.z);
    }
    """
    from tests.utils import ASTGenerator, CodeGenerator
    ast = ASTGenerator(source).generate()
    assert CodeGenerator().generate_and_run(ast) == "12.2votien"


def test_103():
    source = """
    struct Point {
        int x;
        int y;
    };
    void main(){
        Point p;
        p.x = 2;
        printInt(p.x);
    }
    """
    from tests.utils import ASTGenerator, CodeGenerator
    ast = ASTGenerator(source).generate()
    assert CodeGenerator().generate_and_run(ast) == "2"

def test_104():
    source = """
    void main(){
        int a;
        float b;
        string c;
        printInt(a);
        printFloat(b);
        printString(c);
    }
    """
    from tests.utils import ASTGenerator, CodeGenerator
    ast = ASTGenerator(source).generate()
    assert CodeGenerator().generate_and_run(ast) == "00.0"

def test_105():
    source = """
    struct Point {
        int x;
        float y;
        string z;
    };
    void main(){
        Point p;
        printInt(p.x);
        printFloat(p.y);
        printString(p.z);
    }
    """
    from tests.utils import ASTGenerator, CodeGenerator
    ast = ASTGenerator(source).generate()
    assert CodeGenerator().generate_and_run(ast) == "00.0"

def test_106():
    source = """
    foo(int a, int b) {return a + b;}
    void main(){
        auto a; auto b;
        printInt(foo(a, b));
    }
    """
    from tests.utils import ASTGenerator, CodeGenerator
    ast = ASTGenerator(source).generate()
    assert CodeGenerator().generate_and_run(ast) == "0"

def test_107():
    source = """
    void main() {
        // With auto and initialization
        auto x = readInt();
        auto y = readFloat();
        auto name = readString();
    
        // With auto without initialization
        auto sum;
        sum = x + y;              // sum: float (inferred from first usage - assignment)
    
        // With explicit type and initialization
        int count = 0;
        float total = 0.0;
        string greeting = "Hello, ";
    
        // With explicit type without initialization
        int i;
        float f;
        i = readInt();            // assignment to int
        f = readFloat();          // assignment to float
    
        printFloat(sum);
        printString(greeting);
        printString(name);
    }
    """
    from tests.utils import ASTGenerator, CodeGenerator
    ast = ASTGenerator(source).generate()
    assert CodeGenerator().generate_and_run(ast, "4\n0.2\nvotien\n1\n1.0\n") == "4.2Hello, votien"

def test_108():
    source = """
    void main() {
        int i = 0;
        while (i < 5) {
            i = i + 1;
            switch (i) {
                case 2: continue;
                case 4: break;
                default: printInt(i);
            }
            printInt(i);
        }
    }
    """
    from tests.utils import ASTGenerator, CodeGenerator
    ast = ASTGenerator(source).generate()
    assert CodeGenerator().generate_and_run(ast) == "1133455"

def test_109():
    source = """
    void main() {
        int i = 2;
        switch (i) {
            default: int i = 3;
        }
        printInt(i);
    }
    """
    from tests.utils import ASTGenerator, CodeGenerator
    ast = ASTGenerator(source).generate()
    assert CodeGenerator().generate_and_run(ast) == "2"


def test_110():
    source = """
    void main() {
        int a = 5;
        printInt(++a);  // 6
        printInt(a);    // 6
        printInt(--a);  // 5
        printInt(a);    // 5
        printInt(+ + +a);   // 5
        printInt(- - -a);   // -5
    }
    """
    from tests.utils import ASTGenerator, CodeGenerator
    ast = ASTGenerator(source).generate()
    assert CodeGenerator().generate_and_run(ast) == "66555-5"

def test_111():
    source = """
    int factorial(int n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    void main() {
        auto num = 10;
        auto result = factorial(num);
        printInt(result);
    }
    """
    from tests.utils import ASTGenerator, CodeGenerator
    ast = ASTGenerator(source).generate()
    assert CodeGenerator().generate_and_run(ast) == "3628800"

def test_112():
    source = """
    void main() {
        int x = 3;
        switch (x) {
            case 1: printInt(1);
            case 3: printInt(3);
            case 5: printInt(5);
            default: printInt(7);
        }
    }
    """
    from tests.utils import ASTGenerator, CodeGenerator
    ast = ASTGenerator(source).generate()
    assert CodeGenerator().generate_and_run(ast) == "357"

def test_113():
    source = """
    void main() {
        int x = 5;
        switch (x) {
            case 1: printInt(1);
            case 3: printInt(3);
            case 5: int b = 2; printInt(b);
            default: b = 3; printInt(b);
        }
    }
    """
    from tests.utils import ASTGenerator, CodeGenerator
    ast = ASTGenerator(source).generate()
    assert CodeGenerator().generate_and_run(ast) == "23"
