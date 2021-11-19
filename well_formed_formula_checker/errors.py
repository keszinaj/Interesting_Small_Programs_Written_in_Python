#made by keszinaj
'''
   errors implementation
'''

class VariableDeclerationError(Exception):
    def __init__(self, var):
        self.var = var
    def __str__(self):
        return f'Variable {self.var} is not declered'
        
class OperationInvokeError(Exception):
    def __init__(self, operation):
        self.operation = operation
    def __str__(self):
        return f'Operation {self.operation} can not be done'