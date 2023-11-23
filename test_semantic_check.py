from src.COOL.token.program import *
from src.COOL.token.method import Method
from src.COOL.token.attribute import Attribute


a = Attribute(type='object', id='a')
b = Attribute(type='String', id='b')
c = Attribute(type='A', id='c')
d = Attribute(type='Int', id='d')
ma = Method(type='object', id='a', formals=[], expr=None)
mb = Method(type='A', id='b', formals=[], expr=None)
mc = Method(type='object', id='c', formals=[], expr=None)

classa = Class(1, [a, b, mc], "A")
classb = Class(10, [], "B", "A"),
classc = Class(100, [], "C", "B"),
classd = Class(1000, [], "D", "C")

prog = Program(classes=[])

prog.check()
