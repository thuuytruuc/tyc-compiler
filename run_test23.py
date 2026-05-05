from tests.utils import ASTGenerator, CodeGenerator
import os, subprocess
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
ast = ASTGenerator(source).generate()
cg = CodeGenerator()
cg._cleanup_generated_files()
os.chdir(cg.runtime_dir)
cg.codegen.visit(ast)
import glob
for j_file in glob.glob('TyC.j'):
    with open(j_file, 'r') as f:
        print(f"=== {j_file} ===")
        print(f.read())
