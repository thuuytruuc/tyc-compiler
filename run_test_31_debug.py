import sys
from tests.utils import ASTGenerator, CodeGenerator
import os

def trace_pop(self):
    self.curr_op_stack_size -= 1
    if self.curr_op_stack_size < 0:
        raise Exception("Pop empty stack")
    # print("Popped, size is", self.curr_op_stack_size)

def trace_push(self):
    self.curr_op_stack_size += 1
    # print("Pushed, size is", self.curr_op_stack_size)

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

from src.codegen.frame import Frame
Frame.pop = trace_pop
Frame.push = trace_push

def my_visit_func_call(self, node, o=None):
    frame = o.frame
    fn_sym = self.functions[node.name]
    fn_type = fn_sym.type
    code = ""
    print(f"Before evaluating args for {node.name}, stack size: {frame.curr_op_stack_size}")
    for arg in node.args:
        arg_code, _ = self.visit(arg, o)
        code += arg_code
    print(f"After evaluating args for {node.name}, stack size: {frame.curr_op_stack_size}")
    code += self.emit.emit_invoke_static(f"{fn_sym.value.value}/{node.name}", fn_type, frame)
    print(f"After invoke_static for {node.name}, stack size: {frame.curr_op_stack_size}")
    return code, fn_type.return_type

cg.codegen.visit_func_call = my_visit_func_call.__get__(cg.codegen)

try:
    cg.codegen.visit(ast)
except Exception as e:
    import traceback
    traceback.print_exc()
