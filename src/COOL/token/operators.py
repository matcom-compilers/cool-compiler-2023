from numbers import Number as NUM
from token.token import *

class Operators(Token):

    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        self.op1 = op1
        self.op2 = op2
        super().__init__(name, value, line)

    def run():
        pass

class add(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)

    def run(self):
        return self.op1 + self.op2


class sub(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)

    def run(self):
        return self.op1 - self.op2

class mult(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)

    def run(self):
        return self.op1 * self.op2

class div(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)

    def run(self):
        return self.op1 / self.op2
    
class mod(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)

    def run(self):
        return self.op1 % self.op2  
    
class pow(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)

    def run(self):
        return self.op1 ** self.op2 
    
class eq(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)

    def run(self):
        if self.op1 == self.op2:
            return True
        else:
            return False
        
class neq(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)
    
    def run(self):
        if self.op1 != self.op2:
            return True
        else:
            return False
        
class lt(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)
    
    def run(self):
        if self.op1 < self.op2:
            return True
        else:
            return False
        
class leq(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)
    
    def run(self):
        if self.op1 <= self.op2:
            return True
        else:
            return False
        
class gt(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)
    
    def run(self):
        if self.op1 > self.op2:
            return True
        else:
            return False
        
class geq(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:NUM, op2:NUM) -> None:
        super().__init__(name, value, line, op1, op2)
    
    def run(self):
        if self.op1 >= self.op2:
            return True
        else:
            return False
        
class and_(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:bool, op2:bool) -> None:
        super().__init__(name, value, line, op1, op2)
    
    def run(self):
        if self.op1 and self.op2:
            return True
        else:
            return False    
        
class or_(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:bool, op2:bool) -> None:
        super().__init__(name, value, line, op1, op2)
    
    def run(self):
        if self.op1 or self.op2:
            return True
        else:
            return False
        
class not_(Operators):
    def __init__(self, name: str, value: Any, line: int, op1:bool) -> None:
        super().__init__(name, value, line, op1, None)
    
    def run(self):
        if not self.op1:
            return True
        else:
            return False
        
