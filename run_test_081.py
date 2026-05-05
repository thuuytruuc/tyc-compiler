from tests.utils import ASTGenerator, CodeGenerator
import os

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

cg = CodeGenerator()
ast = ASTGenerator(source).generate()
cg._cleanup_generated_files()
os.chdir(cg.runtime_dir)
cg.codegen.visit(ast)
