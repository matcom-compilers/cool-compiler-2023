from src.COOL import CoolLexer
from src.COOL import CoolParser
from src.COOL import Semantic
from src.COOL import Codegen
from src.COOL.token import Program
from src.COOL.utils import load_file


file =\
"""

-- test class with atributtes
class A {
    a: Int;
    b: Int <- 2+2;
    c: Int <- 2-2;
    d: Int <- 2*2;
    e: Int <- 2/2;
    f: Int <- ~2;
    g: Bool <- not true;
    h: Bool <- 2<2;
    i: Bool <- 2<=2;
    j: Bool <- 2=2;
};

-- test class with inheritance and methods
class B inherits A {
    a(): Int { 2 };
    b(aa: Int, bb: Int): Int { 2 };
};

-- test
class C{
    a(): Int {
        2
    };
};

"""

print("\n    COOL Compiler")
print("\n    =====================")
lexer = CoolLexer()

print("\n    Parser:")
parser = CoolParser()
program: Program  = parser.parse(lexer.tokenize(file))

for i in program.classes:
    print("class: ", i.type)
    print("line: ", i.line)
    print("inherits: ", i.inherits)
    # print("features: ", i.features)
    for j in i.features:
        print("    feature: ", j.id)
        print("    expr: ", j.expr)
        if j.__dict__.get("formals", None) is not None:
            print("    formals: ", j.formals)
        print("----------")
    print()

# Semantic.check(program)
# Codegen.check(program)
