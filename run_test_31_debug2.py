import sys
from tests.utils import ASTGenerator, CodeGenerator
import os

source = """
foo(int a, int b) {return a + b;}
void main(){
    auto a; auto b;
    printInt(foo(a, b));
}
"""
ast = ASTGenerator(source).generate()
cg = CodeGenerator()
cg._cleanup_generated_files()
os.chdir(cg.runtime_dir)

original_visit_func_call = cg.codegen.visit_func_call

def my_visit_func_call(self, node, o=None):
    fn_sym = self.functions[node.name]
    print(f"return type of {node.name}: {type(fn_sym.type.return_type)}")
    return original_visit_func_call(node, o)

cg.codegen.visit_func_call = my_visit_func_call.__get__(cg.codegen)

try:
    cg.codegen.visit(ast)
except Exception as e:
    pass
