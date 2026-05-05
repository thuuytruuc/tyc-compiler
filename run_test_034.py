from tests.utils import ASTGenerator, CodeGenerator
import os

source = """
    void main() {
        auto x = readInt();
        auto y = readFloat();
        auto name = readString();
        auto sum;
        sum = x + y;              // sum: float (inferred from first usage - assignment)
        int count = 0;
        float total = 0.0;
        string greeting = "Hello, ";
        int i;
        float f;
        i = readInt();            // assignment to int
        f = readFloat();          // assignment to float
        printFloat(sum);
        printString(greeting);
        printString(name);
    }
"""

cg = CodeGenerator()
ast = ASTGenerator(source).generate()
cg._cleanup_generated_files()
os.chdir(cg.runtime_dir)
cg.codegen.visit(ast)
os.system("cat TyC.j")
print("Compiling TyC.j...")
os.system("java -jar jasmin.jar TyC.j")
print("Running JVM Verification...")
os.system("java TyC")
