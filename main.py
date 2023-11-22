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
    a: A;
    b: B <- 3;
};

-- test class with inheritance and methods
class B inherits A {
    c(): C {
        3
    };

    d(a: A, b: B): D {
        3
    };
};

-- test
class C{

}

"""

print("\n    COOL Compiler")
print("\n    =====================")
lexer = CoolLexer()

print("    Parser:")
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