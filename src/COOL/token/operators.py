from numbers import Number as NUM
from src.COOL.token.token import Token,Any

class Operators(Token):

    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        self.op1 = op1
        self.op2 = op2
        super().__init__(name, value, line)

    def run():
        pass

class Add(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)

    def run(self):
        return self.op1 + self.op2


class Sub(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)

    def run(self):
        return self.op1 - self.op2

class Mult(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)

    def run(self):
        return self.op1 * self.op2

class Div(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)

    def run(self):
        return self.op1 / self.op2
    
# class Mod(Operators):
#     def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
#         super().__init__(name, value, line, op1, op2)

#     def run(self):
#         return self.op1 % self.op2  
    
# class Pow(Operators):
#     def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
#         super().__init__(name, value, line, op1, op2)

#     def run(self):
#         return self.op1 ** self.op2 
    
# class Eq(Operators):
#     def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
#         super().__init__(name, value, line, op1, op2)

#     def run(self):
#         if self.op1 == self.op2:
#             return True
#         else:
#             return False
        
# class Neq(Operators):
#     def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
#         super().__init__(name, value, line, op1, op2)
    
#     def run(self):
#         if self.op1 != self.op2:
#             return True
#         else:
#             return False
        
# class Lt(Operators):
#     def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
#         super().__init__(name, value, line, op1, op2)
    
#     def run(self):
#         if self.op1 < self.op2:
#             return True
#         else:
#             return False
        
# class Leq(Operators):
#     def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
#         super().__init__(name, value, line, op1, op2)
    
#     def run(self):
#         if self.op1 <= self.op2:
#             return True
#         else:
#             return False
        
# class Gt(Operators):
#     def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
#         super().__init__(name, value, line, op1, op2)
    
#     def run(self):
#         if self.op1 > self.op2:
#             return True
#         else:
#             return False
        
# class Geq(Operators):
#     def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
#         super().__init__(name, value, line, op1, op2)
    
#     def run(self):
#         if self.op1 >= self.op2:
#             return True
#         else:
#             return False
        
# class And_(Operators):
#     def __init__(self, name: str, value: Any, line: int, op1:bool, op2:bool) -> None:
#         super().__init__(name, value, line, op1, op2)
    
#     def run(self):
#         if self.op1 and self.op2:
#             return True
#         else:
#             return False    
        
# class Or_(Operators):
#     def __init__(self, name: str, value: Any, line: int, op1:bool, op2:bool) -> None:
#         super().__init__(name, value, line, op1, op2)
    
#     def run(self):
#         if self.op1 or self.op2:
#             return True
#         else:
#             return False
        
# class Not_(Operators):
#     def __init__(self, name: str, value: Any, line: int, op1:bool) -> None:
#         super().__init__(name, value, line, op1, None)
    
#     def run(self):
#         if not self.op1:
#             return True
#         else:
#             return False
        
