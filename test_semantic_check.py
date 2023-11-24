import sys
module = "./src/COOL/"
sys.path.append(module)


from src.COOL.nodes.feature import Method, Attribute
from src.COOL.nodes.program import *

a = Attribute(1, type='object', id='a')
b = Attribute(2, type='String', id='a')
c = Attribute(3, type='A', id='c')
d = Attribute(4, type='Int', id='d')
ma = Method(5, type='object', id='a', formals=[], expr=None)
mb = Method(6, type='A', id='b', formals=[], expr=None)
mc = Method(7, type='object', id='c', formals=[], expr=None)

classa = Class(1, [a, b, ma, mc], "A")
classb = Class(10, [a, b], "B", "A")
classc = Class(100, [], "C", "B")
classd = Class(1000, [], "D", "C")

prog = Program(classes=[classa, classb, classc, classd])

prog.check()
