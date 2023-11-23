import sys
module = "./src/COOL/"
sys.path.append(module)

from src.COOL import CoolLexer
from src.COOL import CoolParser
from src.COOL import Semantic
from src.COOL import Codegen
from src.COOL.tokens import Program
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
    a: String <- "string";
}; -- 14

-- test class with inheritance and methods
class B inherits A {
    a(): Int { 2 };
    b(aa: Int, bb: Int): Int { 2 };
}; -- 20

-- test
class C{
    a(): Int {
        {
            if 1=1 then 2+2 else 3+3 fi;
            while true loop true pool;
            let a: Int in 2;
            let a: Int, b: Int in 2;
            let a: Int <- 3 in 2;
            case true of a: Int => 2; esac;
            case true of a: Int => 2; b: Int => 3; esac;
            new B;
            isvoid 2+2;
            a;
            2+2.a();
            2+2.a(true, 2);
            2+2@Int.a();
            a();
            a(true, 1);
        }
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
