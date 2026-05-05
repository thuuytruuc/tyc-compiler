from tests.utils import ASTGenerator, CodeGenerator
import os

source = """
    void main() {
        int i = 2;
        switch (i) {
            default: int i = 3;
        }
        printInt(i);
    }
"""

cg = CodeGenerator()
ast = ASTGenerator(source).generate()
cg._cleanup_generated_files()
os.chdir(cg.runtime_dir)
cg.codegen.visit(ast)
print("--- TyC.j ---")
os.system("cat TyC.j")
print("--- Compilation and Run ---")
os.system("java -jar jasmin.jar TyC.j")
os.system("java TyC")
