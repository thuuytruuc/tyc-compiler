from tests.utils import ASTGenerator, CodeGenerator
def test_029():
    source = """
    struct Point {
        int x;
        float y;
        string z ;
    };
    void main(){
        Point p = {1,2.2,"votien"};
        printInt(p.x);
        printFloat(p.y);
        printString(p.z);
    }
    """
    ast = ASTGenerator(source).generate()
    return CodeGenerator().generate_and_run(ast)

def test_021():
    source = """
    void main() {
        int x = 3;
        {
            int x = 2;
        }
        printInt(x);
    }
    """
    ast = ASTGenerator(source).generate()
    return CodeGenerator().generate_and_run(ast)

print("test_029:", test_029())
print("test_021:", test_021())
