from tests.utils import ASTGenerator, CodeGenerator
import os, subprocess
source = """
void main(){
    int x;
    printInt(x);
}
"""
ast = ASTGenerator(source).generate()
cg = CodeGenerator()
cg._cleanup_generated_files()
os.chdir(cg.runtime_dir)
cg.codegen.visit(ast)
import glob
for j_file in glob.glob('TyC.j'):
    with open(j_file, 'r') as f:
        content = f.read()
print(CodeGenerator().generate_and_run(ast))
