import sys
module = "./src/COOL/"
sys.path.append(module)


from src.COOL.nodes.feature import Method, Attribute
from src.COOL.nodes.program import *

a = Attribute(1, type='object', id='a')
b = Attribute(2, type='String', id='b')
c = Attribute(3, type='A', id='c')
d = Attribute(4, type='Int', id='d')
ma = Method(5, type='object', id='al', formals=[], expr=None)
mb = Method(6, type='A', id='b', formals=[], expr=None)
mc = Method(7, type='object', id='cd', formals=[], expr=None)

classa = Class(1, [a, ma, mc], "A")
classb = Class(10, [b, c], "B", "A")
classc = Class(100, [], "C", "B")
classd = Class(1000, [], "D", "A")

prog = Program(classes=[classa, classb, classc, classd])

prog.check()
