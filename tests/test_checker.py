"""
Test cases for TyC Static Semantic Checker

100 test cases covering all 8 error types and valid programs.
"""

from tests.utils import Checker


# ============================================================================
# VALID PROGRAMS (test_001 - test_025)
# ============================================================================

def test_001():
    """Valid: simple int variable declaration and use."""
    source = """
void main() {
    int x = 5;
    int y = x + 1;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_002():
    """Valid: auto type inference from int literal."""
    source = """
void main() {
    auto x = 10;
    auto y = 3;
    auto z = x + y;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_003():
    """Valid: function with return and call."""
    source = """
int add(int x, int y) {
    return x + y;
}
void main() {
    int sum = add(5, 3);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_004():
    """Valid: struct declaration and member assignment."""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p;
    p.x = 10;
    p.y = 20;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_005():
    """Valid: nested blocks with shadowing local variables."""
    source = """
void main() {
    int x = 10;
    {
        int y = 20;
        int z = x + y;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_006():
    """Valid: while loop with break and continue."""
    source = """
void main() {
    int i = 0;
    while (i < 10) {
        if (i == 5) {
            break;
        }
        i = i + 1;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_007():
    """Valid: for loop with auto init."""
    source = """
void main() {
    int s = 0;
    for (auto i = 0; i < 5; i++) {
        s = s + i;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_008():
    """Valid: switch statement with int expression."""
    source = """
void main() {
    int day = 2;
    switch (day) {
        case 1: printInt(1); break;
        case 2: printInt(2); break;
        default: printInt(0);
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_009():
    """Valid: built-in functions readInt/printInt."""
    source = """
void main() {
    int x = readInt();
    printInt(x);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_010():
    """Valid: auto inferred from assignment (first use)."""
    source = """
void main() {
    auto a;
    a = 10;
    auto b;
    b = 3.14;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_011():
    """Valid: struct with float and string members."""
    source = """
struct Person {
    string name;
    int age;
};
void main() {
    Person p;
    p.age = 25;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_012():
    """Valid: chained assignment expression."""
    source = """
void main() {
    int a;
    int b;
    int c;
    a = b = c = 10;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_013():
    """Valid: function with void return."""
    source = """
void greet() {
    printString("hello");
    return;
}
void main() {
    greet();
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_014():
    """Valid: relational expression used as int condition."""
    source = """
void main() {
    int x = 5;
    int y = 10;
    if (x < y) {
        printInt(x);
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_015():
    """Valid: struct same name as function (separate namespaces)."""
    source = """
struct foo {
    int x;
};
int foo(int x, int y) {
    return x + y;
}
void main() {
    int r = foo(1, 2);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_016():
    """Valid: auto variable inferred from printInt param."""
    source = """
void main() {
    auto x;
    printInt(x);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_017():
    """Valid: inner block shadows outer local variable."""
    source = """
void main() {
    int value = 100;
    {
        int value = 200;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_018():
    """Valid: logical operators with int operands."""
    source = """
void main() {
    int a = 1;
    int b = 0;
    int c = a && b;
    int d = a || b;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_019():
    """Valid: prefix/postfix increment on int."""
    source = """
void main() {
    int x = 5;
    ++x;
    x++;
    --x;
    x--;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_020():
    """Valid: float arithmetic."""
    source = """
void main() {
    float a = 1.5;
    float b = 2.5;
    float c = a + b;
    float d = a * b;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_021():
    """Valid: int + float = float result."""
    source = """
void main() {
    int a = 5;
    float b = 3.14;
    float c = a + b;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_022():
    """Valid: modulus operator with ints."""
    source = """
void main() {
    int a = 10;
    int b = 3;
    int c = a % b;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_023():
    """Valid: nested struct (struct using another struct type)."""
    source = """
struct Address {
    string street;
};
struct Person {
    string name;
    Address addr;
};
void main() {
    Person p;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_024():
    """Valid: auto inferred from one side of binary op — int literal."""
    source = """
void main() {
    auto value;
    auto result = value + 5;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_025():
    """Valid: auto inferred from parameter type (readFloat)."""
    source = """
void main() {
    auto x;
    x = readFloat();
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


# ============================================================================
# REDECLARED (test_026 - test_038)
# ============================================================================

def test_026():
    """Error: Redeclared struct in global scope."""
    source = """
struct Point { int x; };
struct Point { int y; };
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Struct, Point)"


def test_027():
    """Error: Redeclared function in global scope."""
    source = """
int add(int x, int y) { return x + y; }
int add(int a, int b) { return a + b; }
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Function, add)"


def test_028():
    """Error: Redeclared variable in same block."""
    source = """
void main() {
    int count = 10;
    int count = 20;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, count)"


def test_029():
    """Error: Redeclared parameter in same function signature."""
    source = """
int calc(int x, float y, int x) { return x; }
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Parameter, x)"


def test_030():
    """Error: Local variable reuses parameter name."""
    source = """
void func(int x) {
    int x = 10;
}
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, x)"


def test_031():
    """Error: Redeclared struct member."""
    source = """
struct Bad {
    int x;
    int x;
};
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Member, x)"


def test_032():
    """Error: Redeclared variable in nested block still conflicts with param."""
    source = """
void func(int y) {
    {
        int y = 5;
    }
}
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, y)"


def test_033():
    """Error: Redeclared function (different param count, no overloading)."""
    source = """
void print_val() {}
void print_val(int x) {}
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Function, print_val)"


def test_034():
    """Error: Two variables with same name in same block."""
    source = """
void main() {
    float ratio = 1.0;
    float ratio = 2.0;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, ratio)"


def test_035():
    """Error: Struct re-declared even though first had no members."""
    source = """
struct Empty {};
struct Empty { int x; };
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Struct, Empty)"


def test_036():
    """Error: Redeclared member (string type)."""
    source = """
struct S {
    string name;
    string name;
};
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Member, name)"


def test_037():
    """Error: auto variable re-declared in same block."""
    source = """
void main() {
    auto x = 1;
    auto x = 2;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, x)"


def test_038():
    """Error: re-using parameter name inside deeply nested block."""
    source = """
void deep(int val) {
    {
        {
            int val = 99;
        }
    }
}
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, val)"


# ============================================================================
# UNDECLARED IDENTIFIER (test_039 - test_045)
# ============================================================================

def test_039():
    """Error: UndeclaredIdentifier — variable used before declaration."""
    source = """
void main() {
    int result = undeclaredVar + 10;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(undeclaredVar)"


def test_040():
    """Error: UndeclaredIdentifier — used in different function scope."""
    source = """
void func1() {
    int local = 42;
}
void main() {
    int val = local + 1;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(local)"


def test_041():
    """Error: UndeclaredIdentifier — used out-of-scope (after block)."""
    source = """
void main() {
    {
        int inner = 5;
    }
    int x = inner + 1;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(inner)"


def test_042():
    """Error: UndeclaredIdentifier — used before its own declaration."""
    source = """
void main() {
    int x = y + 5;
    int y = 10;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(y)"


def test_043():
    """Error: UndeclaredIdentifier — assignment to undeclared var."""
    source = """
void main() {
    ghost = 100;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(ghost)"


def test_044():
    """Error: UndeclaredIdentifier in if condition."""
    source = """
void main() {
    if (undefined_cond) {
        printInt(1);
    }
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(undefined_cond)"


def test_045():
    """Error: UndeclaredIdentifier in return expression."""
    source = """
int compute() {
    return missing;
}
void main() {}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(missing)"


# ============================================================================
# UNDECLARED FUNCTION (test_046 - test_050)
# ============================================================================

def test_046():
    """Error: UndeclaredFunction — calling function that doesn't exist."""
    source = """
void main() {
    int r = calculate(5, 3);
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(calculate)"


def test_047():
    """Error: UndeclaredFunction — function called from main but declared after (grammar processes structs first but functions sequentially)."""
    source = """
void main() {
    int v = add(10, 20);
}
int add(int x, int y) { return x + y; }
"""
    # Both main and add are functions; main is processed first, but add is not yet registered.
    assert Checker(source).check_from_source() == "UndeclaredFunction(add)"


def test_048():
    """Error: UndeclaredFunction — typo in built-in name."""
    source = """
void main() {
    printint(42);
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(printint)"


def test_049():
    """Error: UndeclaredFunction inside another function."""
    source = """
void helper() {
    int x = doSomething();
}
void main() {}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(doSomething)"


def test_050():
    """Error: UndeclaredFunction passed as argument context."""
    source = """
void main() {
    printInt(badFunc());
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(badFunc)"


# ============================================================================
# UNDECLARED STRUCT (test_051 - test_055)
# ============================================================================

def test_051():
    """Error: UndeclaredStruct — struct member uses a struct not yet declared."""
    source = """
struct Container {
    Item item;
};
void main() {}
"""
    # 'Item' struct is not declared anywhere
    assert Checker(source).check_from_source() == "UndeclaredStruct(Item)"


def test_052():
    """Error: UndeclaredStruct — struct member uses undeclared struct."""
    source = """
struct Address {
    City city;
};
struct City { string name; };
void main() {}
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(City)"


def test_053():
    """Error: UndeclaredStruct — parameter has unknown struct type."""
    source = """
void process(Unknown p) {}
void main() {}
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(Unknown)"


def test_054():
    """Error: UndeclaredStruct — return type of function is unknown struct."""
    source = """
Ghost getGhost() { }
void main() {}
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(Ghost)"


def test_055():
    """Error: UndeclaredStruct — used in local var decl."""
    source = """
void main() {
    Phantom x;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(Phantom)"


# ============================================================================
# TYPE CANNOT BE INFERRED (test_056 - test_065)
# ============================================================================

def test_056():
    """Error: TypeCannotBeInferred — two unresolved autos in binary op."""
    source = """
void main() {
    auto x;
    auto y;
    auto result = x + y;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_057():
    """Error: TypeCannotBeInferred — assignment of two unknown autos."""
    source = """
void main() {
    auto x;
    auto y;
    x = y;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_058():
    """Error: TypeCannotBeInferred — auto never used (block end)."""
    source = """
void main() {
    auto x;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_059():
    """Error: TypeCannotBeInferred — return unknown auto."""
    source = """
int get() {
    auto x;
    return x;
}
void main() {}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_060():
    """Error: TypeCannotBeInferred — comparison of two unknown autos."""
    source = """
void main() {
    auto x;
    auto y;
    int r = x < y;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_061():
    """Error: TypeCannotBeInferred — multiplication of two unknown autos."""
    source = """
void main() {
    auto a;
    auto b;
    int c = a * b;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_062():
    """Error: TypeMismatchInExpression — auto x + string literal (x inferred as string, but + not valid on strings)."""
    source = """
void main() {
    auto x;
    auto y;
    auto result = x + "hello";
}
"""
    result = Checker(source).check_from_source()
    # x gets inferred as string from "hello", but string + string is not valid (not numeric)
    assert result.startswith("TypeMismatchInExpression(") or result.startswith("TypeCannotBeInferred(")


def test_063():
    """Error: TypeCannotBeInferred — mutually dependent autos."""
    source = """
void main() {
    auto a;
    auto b;
    a = b;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_064():
    """Error: TypeCannotBeInferred — auto declared but unused in nested block."""
    source = """
void main() {
    {
        auto z;
    }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_065():
    """Error: TypeCannotBeInferred — two autos: logical and."""
    source = """
void main() {
    auto p;
    auto q;
    int r = p && q;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


# ============================================================================
# TYPE MISMATCH IN STATEMENT (test_066 - test_078)
# ============================================================================

def test_066():
    """Error: TypeMismatchInStatement — float condition in if."""
    source = """
void main() {
    float x = 5.0;
    if (x) {
        printInt(1);
    }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")

def test_067():
    """Error: TypeMismatchInStatement — string condition in while."""
    source = """
void main() {
    string msg = "loop";
    while (msg) {
        break;
    }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_068():
    """Error: TypeMismatchInStatement — int assigned to string var."""
    source = """
void main() {
    string text = "hello";
    text = 42;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_069():
    """Error: TypeMismatchInStatement — string returned from int function."""
    source = """
int getValue() {
    return "invalid";
}
void main() {}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_070():
    """Error: TypeMismatchInStatement — void function with value return."""
    source = """
void doWork() {
    return 10;
}
void main() {}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_071():
    """Error: TypeMismatchInStatement — struct assignment type mismatch."""
    source = """
struct Point { int x; int y; };
struct Person { string name; int age; };
void main() {
    Point p;
    Person person;
    p = person;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_072():
    """Error: TypeMismatchInStatement — float condition in for loop."""
    source = """
void main() {
    float f = 1.0;
    for (; f; ) {
        break;
    }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_073():
    """Error: TypeMismatchInStatement — switch on float."""
    source = """
void main() {
    float f = 3.14;
    switch (f) {
        case 1: break;
    }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_074():
    """Error: TypeMismatchInStatement — assigning float to int variable."""
    source = """
void main() {
    int x = 10;
    float y = 3.14;
    x = y;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_075():
    """Error: TypeMismatchInStatement — non-void function returns void (bare return)."""
    source = """
int compute() {
    return;
}
void main() {}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_076():
    """Error: TypeMismatchInStatement — wrong init type for int."""
    source = """
void main() {
    int x = "hello";
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_077():
    """Error: TypeMismatchInStatement — return type mismatch (int expected, float returned)."""
    source = """
int getVal() {
    return 3.14;
}
void main() {}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_078():
    """Error: TypeMismatchInStatement — string condition in while."""
    source = """
void main() {
    float f = 1.5;
    while (f) {
        printFloat(f);
    }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


# ============================================================================
# TYPE MISMATCH IN EXPRESSION (test_079 - test_092)
# ============================================================================

def test_079():
    """Error: TypeMismatchInExpression — adding int and string."""
    source = """
void main() {
    int x = 5;
    string text = "hello";
    int sum = x + text;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_080():
    """Error: TypeMismatchInExpression — modulus with float."""
    source = """
void main() {
    float f = 3.14;
    int x = 10;
    int r = f % x;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_081():
    """Error: TypeMismatchInExpression — logical AND with float."""
    source = """
void main() {
    float f = 3.14;
    int x = 10;
    int r = f && x;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_082():
    """Error: TypeMismatchInExpression — logical NOT on float."""
    source = """
void main() {
    float f = 3.14;
    int r = !f;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_083():
    """Error: TypeMismatchInExpression — increment on float."""
    source = """
void main() {
    float f = 3.14;
    ++f;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_084():
    """Error: TypeMismatchInExpression — postfix decrement on float."""
    source = """
void main() {
    float f = 3.14;
    f--;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_085():
    """Error: TypeMismatchInExpression — member access on non-struct."""
    source = """
void main() {
    int x = 10;
    int val = x.member;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_086():
    """Error: TypeMismatchInExpression — accessing non-existent struct member."""
    source = """
struct Point { int x; int y; };
void main() {
    Point p;
    int z = p.z;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_087():
    """Error: TypeMismatchInExpression — function call arg type mismatch."""
    source = """
void process(int x) {}
void main() {
    string text = "123";
    process(text);
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_088():
    """Error: TypeMismatchInExpression — too few arguments to function."""
    source = """
int add(int x, int y) { return x + y; }
void main() {
    int r = add(10);
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_089():
    """Error: TypeMismatchInExpression — too many arguments to function."""
    source = """
int add(int x, int y) { return x + y; }
void main() {
    int r = add(10, 20, 30);
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_090():
    """Error: TypeMismatchInExpression — relational op on string."""
    source = """
void main() {
    string a = "a";
    string b = "b";
    int r = a < b;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_091():
    """Error: TypeMismatchInExpression — logical OR with float."""
    source = """
void main() {
    float f = 1.0;
    int x = 1;
    int r = f || x;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_092():
    """Error: TypeMismatchInExpression — assignment expr lhs/rhs type mismatch."""
    source = """
void main() {
    int x = 10;
    string text = "hello";
    int result = (x = text) + 5;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


# ============================================================================
# MUST IN LOOP (test_093 - test_100)
# ============================================================================

def test_093():
    """Error: MustInLoop — break outside any loop."""
    source = """
void main() {
    break;
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(BreakStmt())"


def test_094():
    """Error: MustInLoop — continue outside any loop."""
    source = """
void main() {
    continue;
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(ContinueStmt())"


def test_095():
    """Error: MustInLoop — break inside if without surrounding loop."""
    source = """
void main() {
    if (1) {
        break;
    }
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(BreakStmt())"


def test_096():
    """Error: MustInLoop — continue inside switch (not a loop)."""
    source = """
void main() {
    int x = 1;
    switch (x) {
        case 1:
            continue;
            break;
    }
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(ContinueStmt())"


def test_097():
    """Error: MustInLoop — break in function called from loop (no context transfer)."""
    source = """
void helper() {
    break;
}
void main() {
    for (auto i = 0; i < 10; i++) {
        helper();
    }
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(BreakStmt())"


def test_098():
    """Valid: break and continue inside nested for loops."""
    source = """
void main() {
    for (auto i = 0; i < 5; i++) {
        for (auto j = 0; j < 5; j++) {
            if (i == j) {
                continue;
            }
            if (j > 3) {
                break;
            }
        }
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_099():
    """Valid: break inside switch inside while loop."""
    source = """
void main() {
    int i = 0;
    while (i < 10) {
        switch (i) {
            case 5: break;
        }
        i = i + 1;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_100():
    """Valid: comprehensive program — structs, functions, loops, auto inference."""
    source = """
struct Vector {
    int x;
    int y;
};
int dot(Vector a, Vector b) {
    return a.x * b.x + a.y * b.y;
}
void main() {
    Vector v1;
    Vector v2;
    v1.x = 1;
    v1.y = 2;
    v2.x = 3;
    v2.y = 4;
    int result = dot(v1, v2);
    printInt(result);
    for (auto i = 0; i < 5; i++) {
        if (i == 3) {
            break;
        }
        printInt(i);
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"
