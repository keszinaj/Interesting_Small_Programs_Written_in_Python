#made by keszinaj
import itertools
from errors import OperationInvokeError, VariableDeclerationError 

'''
   Main class
'''

class Formula():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        raise OperationInvokeError("to string")
    def __add__(self, other):
        return Or(self, other)
    def __mul__(self, other):
        return And(self, other)
    def calculate(self, variables):
        raise OperationInvokeError("calculate")
    # brute force
    def isTautology(self, env):
        n = len(env)
        #https://www.hackerrank.com/challenges/itertools-product/problem
        product = list(itertools.product([True, False],repeat = n))
        i = 0
        for i in range(len(product)):
            if self.calculate(dict(zip(env, product[i]))) == False:
                return False
        return True

'''
    Logical and
'''

class And(Formula): 
    def __init__(self, left, right):
        super().__init__(left, right)
    def calculate(self, variables):
        return self.left.calculate(variables) and self.right.calculate(variables)
    def simplify(self, var):
        if Neg(self.right).isTautology(var) or Neg(self.left).isTautology(var):
            return LogicalValue(False)
        else:
            return self
    def __str__(self):
            return "(" + str(self.left) + " \u2227 " + str(self.right) + ")"

'''
    Logical Or
'''

class Or(Formula):
    def __init__(self, left, right):
        super().__init__(left, right)
    def calculate(self, variables):
        return self.left.calculate(variables) or self.right.calculate(variables)
    def simplify(self, var):
        if Neg(self.right).isTautology(var):
            return self.left
        elif Neg(self.left).isTautology(var):
            return self.right
        else:
            return self
    def __str__(self):
            return "(" + str(self.left) + " \u2228 " + str(self.right) + ")"

'''
    Logical =>
'''
class Conditional(Formula):
    def __init__(self, left, right):
        super().__init__(left, right)
    # https://www.wolframalpha.com/input/?i=%28p+%3D%3E+q%29+%3C%3D%3Enot+%28p+and+%28not+q%29%29
    def calculate(self, variables):
        return not ((self.left.calculate(variables)) and  not(self.right.calculate(variables)))
    def __str__(self):
            return "(" + str(self.left) + " \u21D2 " + str(self.right) + ")"

'''
    Logical <=>
'''
class Eq(Formula):
    def __init__(self, left, right):
        super().__init__(left, right)
    def calculate(self, variables):
        l = self.left.calculate(variables)
        r = self.right.calculate(variables)
        return (l and r) or (not l and not r)
    def __str__(self):
            return "(" + str(self.left) + " \u21D4  " + str(self.right) + ")"

''' 
    Logical negation
'''

class Neg(Formula):
    def __init__(self, w):
        self.w = w
    def calculate(self, variables):
        return not (self.w.calculate(variables))
    def __str__(self):
            return "(" + "\u00AC" + str(self.w) + ")"
    def __add__(self, other):
        raise OperationInvokeError("add")
    def __mul__(self, other):
        raise OperationInvokeError("mul")

''' 
    Representation of variable
'''

class Variable(Formula):
    def __init__(self, var):
        self.v = var
    def calculate(self, variables):
        try:
            return variables[self.v]
        except:
            raise VariableDeclerationError(self.v)
    def __str__(self):
            return self.v
    def __add__(self, other):
        raise OperationInvokeError("add")
    def __mul__(self, other):
        raise OperationInvokeError("mul")

''' 
    Representation of logical value
'''

class LogicalValue(Formula):
    def __init__(self, lv):
        self.w = lv
    def calculate(self, var):
        return self.w
    def __str__(self):
            return str(self.w)
