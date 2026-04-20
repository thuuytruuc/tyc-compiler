from tests.utils import Checker

# =================================================================
# Valid Programs (Test 1 - 20)
# =================================================================

def test_001():
    source = "void execute() { int valA = 42; int valB = valA + 2; }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_002():
    source = "int computeSum(int a, int b) { return a + b; } void execute() { int total = computeSum(10, 4); }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_003():
    source = "struct Vector { int u; int v; }; void execute() { Vector vec; vec.u = 15; vec.v = 25; }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_004():
    source = "void execute() { int num = 15; { int temp = 25; int res = num + temp; } }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_005():
    source = "void process() { int data = 50; { int data = 150; { int data = 250; } } }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_006():
    source = "void testScope() { int a = 15; { int b = 25; } int b = 35; }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_007():
    source = "void validVar() { int num1 = 15; int num2 = num1 + 5; }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_008():
    source = "int multiply(int m, int n) { int result = m * n; return result; }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_009():
    source = "void scopeTest() { int out = 15; { int in = out + 5; } }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_010():
    source = "int doMath(int a, int b) { return a * b; } void execute() { int res = doMath(10, 5); }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_011():
    source = "void sysCalls() { int a = readInt(); printInt(a); float b = readFloat(); string str = readString(); }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_012():
    source = "struct Item { int id; int price; }; struct Order { string customer; Item item; };"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_013():
    source = "void execute() { for(int idx = 0; idx < 10; idx++) {} for(int idx = 0; idx < 10; idx++) {} }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_014():
    source = "void execute() { int val1; int val2; if (1) { int val1 = val2; } }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_015():
    source = "void execute() { int data; while(1) { int data; } }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_016():
    source = "void execute() { for(int data;;) { int data; } }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_017():
    source = "void execute() { for(int data;;) break; int data; }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_018():
    source = "void execute(){ for (string text; ; ) {} }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_019():
    source = "void execute(){ float val; for (val=2.5; ; ) {} }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_020():
    source = "void execute(){ string text; for (; ; text = \"A\") {} }"
    assert Checker(source).check_from_source() == "Static checking passed"


# =================================================================
# Redeclared & Undeclared Errors (Test 21 - 40)
# =================================================================

def test_021():
    source = "struct Data { int id; }; struct Data { int name; };"
    assert Checker(source).check_from_source() == "Redeclared(Struct, Data)"

def test_022():
    source = "int calc(int a, int b) { return a + b; } int calc(int m, int n) { return m + n; }"
    assert Checker(source).check_from_source() == "Redeclared(Function, calc)"

def test_023():
    source = "void execute() { int amount = 15; int amount = 25; }"
    assert Checker(source).check_from_source() == "Redeclared(Variable, amount)"

def test_024():
    source = "int process(int val1, float val2, int val1) { return val1; }"
    assert Checker(source).check_from_source() == "Redeclared(Parameter, val1)"

def test_025():
    source = "void execute() { int data; if (1) int data = 5; }"
    assert Checker(source).check_from_source() == "Redeclared(Variable, data)"

def test_026():
    source = "void execute() { int item; while(1) int item; }"
    assert Checker(source).check_from_source() == "Redeclared(Variable, item)"

def test_027():
    source = "void execute() { for(int idx;;) int idx; }"
    assert Checker(source).check_from_source() == "Redeclared(Variable, idx)"

def test_028():
    source = "void execute() { int a; switch (1) { case 1: int a; int b; float b; } }"
    assert Checker(source).check_from_source() == "Redeclared(Variable, b)"

def test_029():
    source = "void readFloat() {}"
    assert Checker(source).check_from_source() == "Redeclared(Function, readFloat)"

def test_030():
    source = "void execute(int num) {int num;}"
    assert Checker(source).check_from_source() == "Redeclared(Variable, num)"

def test_031():
    source = "void execute() { int res = unkVar + 15; }"
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(unkVar)"

def test_032():
    source = "void execute() { int a = b + 5; int b = 15; }"
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(b)"

def test_033():
    source = "void f1() { int v1 = 42; } void f2() { int val = v1 + 1; }"
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(v1)"

def test_034():
    source = "void execute() { int res = unkFunc(5, 4); }"
    assert Checker(source).check_from_source() == "UndeclaredFunction(unkFunc)"

def test_035():
    source = "void execute() { int val = doTask(15, 25); } int doTask(int a, int b) { return a + b; }"
    assert Checker(source).check_from_source() == "UndeclaredFunction(doTask)"

def test_036():
    source = "void execute() { Box b; } struct Box { int w; int h; };"
    assert Checker(source).check_from_source() == "UndeclaredStruct(Box)"

def test_037():
    source = "void execute() { Employee emp; } struct Employee { string name; };"
    assert Checker(source).check_from_source() == "UndeclaredStruct(Employee)"

def test_038():
    source = "struct Branch { string name; Region r; }; struct Region { int id; };"
    assert Checker(source).check_from_source() == "UndeclaredStruct(Region)"

def test_039():
    source = "void execute() { int VAL = VAL; }"
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(VAL)"

def test_040():
    source = "void execute() { switch (1) { case unk: } }"
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(unk)"


# =================================================================
# Loop Controls & Statement Errors (Test 41 - 60)
# =================================================================

def test_041():
    source = "void breakError() { break; }"
    assert Checker(source).check_from_source() == "MustInLoop(BreakStmt())"

def test_042():
    source = "void contError() { continue; }"
    assert Checker(source).check_from_source() == "MustInLoop(ContinueStmt())"

def test_043():
    source = "void switchCont() { int val = 1; switch (val) { case 1: break; continue; } }"
    assert Checker(source).check_from_source() == "MustInLoop(ContinueStmt())"

def test_044():
    source = "void execute() { int num = 20; int val = 2.71; int res = num + val; }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(IntType(), val = FloatLiteral(2.71)))"

def test_045():
    source = "void condErr() { float val = 2.5; if (val) { printInt(1); } }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(IfStmt(if Identifier(val) then BlockStmt([ExprStmt(FuncCall(printInt, [IntLiteral(1)]))])))"

def test_046():
    source = "void condErr() { string txt = \"hi\"; if (txt) { printString(txt); } }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(IfStmt(if Identifier(txt) then BlockStmt([ExprStmt(FuncCall(printString, [Identifier(txt)]))])))"

def test_047():
    source = "void whileErr() { float dec = 2.5; while (dec) { printFloat(dec); } }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(WhileStmt(while Identifier(dec) do BlockStmt([ExprStmt(FuncCall(printFloat, [Identifier(dec)]))])))"

def test_048():
    source = "void assignErr() { int num = 15; string txt = \"hi\"; num = txt; }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(AssignExpr(Identifier(num) = Identifier(txt)))"

def test_049():
    source = "void forErr() { int idx = 0; for (idx=1; \"str\"; idx++) {} }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ForStmt(for ExprStmt(AssignExpr(Identifier(idx) = IntLiteral(1))); StringLiteral('str'); PostfixOp(Identifier(idx)++) do BlockStmt([])))"

def test_050():
    source = "void switchErr() { float dec = 2.71; switch (dec) { case 1: break; } }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(SwitchStmt(switch Identifier(dec) cases [CaseStmt(case IntLiteral(1): [BreakStmt()])]))"

def test_051():
    source = "int getVal() { return \"fail\"; }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ReturnStmt(return StringLiteral('fail')))"

def test_052():
    source = "int retErr() { return; }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ReturnStmt(return))"

def test_053():
    source = "int func() { auto var; var = 15; var = 2; var = 2.5; }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(AssignExpr(Identifier(var) = FloatLiteral(2.5)))"

def test_054():
    source = "doTask() { return 1; } int func() { int a; a = doTask(); float b; b = doTask(); }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(AssignExpr(Identifier(b) = FuncCall(doTask, [])))"

def test_055():
    source = "void execute(){ switch(2 || 3){case 2.0: } }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(SwitchStmt(switch BinaryOp(IntLiteral(2), ||, IntLiteral(3)) cases [CaseStmt(case FloatLiteral(2.0): [])]))"

def test_056():
    source = "void execute() { auto var; switch (1){case var:} float b = var; }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case Identifier(var): [])]))"

def test_057():
    source = "void execute() { auto var; int res = 2.5 + var; }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(IntType(), res = BinaryOp(FloatLiteral(2.5), +, Identifier(var))))"

def test_058():
    source = "void execute() { int val = 1; switch (val) { case val: } }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(SwitchStmt(switch Identifier(val) cases [CaseStmt(case Identifier(val): [])]))"

def test_059():
    source = "int func(){return 1;} void execute() { int num = 1; switch (num) { case func(): } }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(SwitchStmt(switch Identifier(num) cases [CaseStmt(case FuncCall(func, []): [])]))"

def test_060():
    source = "struct Vector { int u; int v; }; void execute() { Vector vec = {15}; }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(StructType(Vector), vec = StructLiteral({IntLiteral(15)})))"


# =================================================================
# TypeMismatchInExpression (Test 61 - 80)
# =================================================================

def test_061():
    source = "void badAdd() { int val = 15; string txt = \"str\"; int res = val + txt; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(val), +, Identifier(txt)))"

def test_062():
    source = "void badMul() { int val = 15; string txt = \"str\"; float res = val * txt; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(val), *, Identifier(txt)))"

def test_063():
    source = "void badMod1() { float dec = 2.71; int val = 15 % 2; int res = dec % val; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(dec), %, Identifier(val)))"

def test_064():
    source = "void badMod2() { float dec = 2.71; int val = 15; int res = val % dec; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(val), %, Identifier(dec)))"

def test_065():
    source = "void badRel() { int val = 15 == 1; string txt = \"str\"; int eq = txt == val; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(txt), ==, Identifier(val)))"

def test_066():
    source = "void badRel2() { int val = 15 > 2; string txt = \"str\"; int res = val < txt; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(val), <, Identifier(txt)))"

def test_067():
    source = "void badLog() { float dec = 2.71; int val = 15 && 25; int res = dec && val; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(dec), &&, Identifier(val)))"

def test_068():
    source = "void badLog2() { float dec = 2.71; int val = !15; int n = !dec; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PrefixOp(!Identifier(dec)))"

def test_069():
    source = "void badInc() { float dec = 2.71; ++dec; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PrefixOp(++Identifier(dec)))"

def test_070():
    source = "void badInc2() { float dec = 2.71; dec++; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PostfixOp(Identifier(dec)++))"

def test_071():
    source = "void badOp() { int val = 15; ++val; val++; ++15; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PrefixOp(++IntLiteral(15)))"

def test_072():
    source = "void badOp2() { int val = 15; --(val + 1); }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PrefixOp(--BinaryOp(Identifier(val), +, IntLiteral(1))))"

def test_073():
    source = "void badOp3() { int val = 15; (val + 2)++; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PostfixOp(BinaryOp(Identifier(val), +, IntLiteral(2))++))"

def test_074():
    source = "struct Vector { int u; int v; }; void badMem() { int val = 15; int res = val.mem; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(MemberAccess(Identifier(val).mem))"

def test_075():
    source = "struct Vector { int u; int v; }; void badMem2() { Vector vec = {15, 25}; int invalid = vec.w; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(MemberAccess(Identifier(vec).w))"

def test_076():
    source = "void process(int val) { } void badCall() { string txt = \"123\"; process(txt); }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(FuncCall(process, [Identifier(txt)]))"

def test_077():
    source = "int compute(int a, int b) { return a + b; } void badArg() { int res = compute(15); }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(FuncCall(compute, [IntLiteral(15)]))"

def test_078():
    source = "int compute(int a, int b) { return a + b; } void badArg2() { int res = compute(15, 25, 35); }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(FuncCall(compute, [IntLiteral(15), IntLiteral(25), IntLiteral(35)]))"

def test_079():
    source = "void badAssign() { int val = 15; string txt = \"hi\"; int res = (val = txt) + 5; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(AssignExpr(Identifier(val) = Identifier(txt)))"

def test_080():
    source = "void execute() { 42 = 99; }"
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


# =================================================================
# TypeCannotBeInferred & Auto Logic (Test 81 - 100)
# =================================================================

def test_081():
    source = "int execute() { auto var1; auto var2; var1 = var2; }"
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(AssignExpr(Identifier(var1) = Identifier(var2)))"

def test_082():
    source = "int execute() { auto var1; auto var2; {{{ var2 && var1; }}} var2 = 2; var1 = 2.5; }"
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BinaryOp(Identifier(var2), &&, Identifier(var1)))"

def test_083():
    source = "void execute() { auto var1; auto var2; int res = var1 + var2; }"
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BinaryOp(Identifier(var1), +, Identifier(var2)))"

def test_084():
    source = "void execute() { auto var1; auto var2; int res = 1 + var2; }"
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BlockStmt([VarDecl(auto, var1), VarDecl(auto, var2), VarDecl(IntType(), res = BinaryOp(IntLiteral(1), +, Identifier(var2)))]))"

def test_085():
    source = "void execute() { auto var2; int res = var2 > 2; }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_086():
    source = "void execute() { auto var1; + var1; float var2 = var1; }"
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(PrefixOp(+Identifier(var1)))"

def test_087():
    source = "void execute() { auto var1; auto var2; var1 = 1; var1 + var2; }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_088():
    source = "task() { auto var1; return var1;} void execute() { auto var1 = task(); float var2 = var1; }"
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(ReturnStmt(return Identifier(var1)))"

def test_089():
    source = "void unused() { auto data; }"
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BlockStmt([VarDecl(auto, data)]))"

def test_090():
    source = "void unused() { auto var1; auto var2; { var1 && var2; } auto var3; }"
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BinaryOp(Identifier(var1), &&, Identifier(var2)))"

def test_091():
    source = "void unused() { switch (1) { case 1: auto data; } }"
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case IntLiteral(1): [VarDecl(auto, data)])]))"

def test_092():
    source = "void execute() { auto var2; float res = var2 + 2.5; }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_093():
    source = "task() { int var1 = task(); return 1; }"
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(FuncCall(task, []))"

def test_094():
    source = "void execute() { string txt = \"hi\"; auto neg = -txt; }"
    assert "TypeMismatch" in Checker(source).check_from_source()

def test_095():
    source = "void execute() { int num = 1; switch (num) { case - 1: case 1 + 2: case - 2: case 1 || 2 * 3 / 4 + 2: } }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_096():
    source = "int task(){return 1;} void execute() { int val; switch (task()) { case val = 1: } }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(SwitchStmt(switch FuncCall(task, []) cases [CaseStmt(case AssignExpr(Identifier(val) = IntLiteral(1)): [])]))"

def test_097():
    source = "void execute() { int val; int num; if (1) { int val = num; } }"
    assert Checker(source).check_from_source() == "Static checking passed"

def test_098():
    source = "void execute(int val, int num) { val = num; { int val; val = item; } }"
    assert Checker(source).check_from_source() == "Redeclared(Variable, val)"

def test_099():
    source = "void execute() { int item = 15; string text = \"abc\"; int res = item + text; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(item), +, Identifier(text)))"

def test_100():
    source = "void execute() { auto ptr; int value = 1; auto data; value = ptr + data; }"
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BinaryOp(Identifier(ptr), +, Identifier(data)))"

# =================================================================
# Edge Cases based on Strict TyC Specification (Test 101 - 110)
# =================================================================

def test_101():
    source = """
    struct Controller { int id; };
    int Controller() { return 1; }
    void main() { 
        Controller c; 
        int val = Controller(); 
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_102():
    source = "struct Node { int val; Node next; }; void main() {}"
    assert Checker(source).check_from_source() == "UndeclaredStruct(Node)"

def test_103():
    source = """
    task() { 
        return 1; 
        return 2.5; 
    } 
    void main() {}
    """
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ReturnStmt(return FloatLiteral(2.5)))"

def test_104():
    source = """
    task() { 
        return; 
        return 1; 
    } 
    void main() {}
    """
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ReturnStmt(return IntLiteral(1)))"

def test_105():
    source = "void main() { float f = 5; }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(FloatType(), f = IntLiteral(5)))"

def test_106():
    source = "void process(float f) {} void main() { process(10); }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(FuncCall(process, [IntLiteral(10)]))"

def test_107():
    source = "void main() { int a; float b; a = b = 3.14; }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(AssignExpr(Identifier(a) = AssignExpr(Identifier(b) = FloatLiteral(3.14))))"

def test_108():
    source = "void main() { int x = 1; (x + 1) = 2; }"
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(AssignExpr(BinaryOp(Identifier(x), +, IntLiteral(1)) = IntLiteral(2)))"

def test_109():
    source = "void main() { int x = 1; switch(x) { case 1.5: break; } }"
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(SwitchStmt(switch Identifier(x) cases [CaseStmt(case FloatLiteral(1.5): [BreakStmt()])]))"

def test_110():
    source = """
    void main() { 
        auto unknown; 
        auto result = unknown + 5; 
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"