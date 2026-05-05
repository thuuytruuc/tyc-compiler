from tests.utils import ASTGenerator, CodeGenerator
source = """
    void main() {
        auto sum;
        sum = 1.0;
    }
"""
ast = ASTGenerator(source).generate()
for stmt in ast.decls[0].body.statements:
    if stmt.__class__.__name__ == 'VarDecl':
        print(f"VarDecl: {stmt.name}, type: {stmt.var_type}")
