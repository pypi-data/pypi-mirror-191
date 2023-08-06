class FunctionNotFoundException(Exception):
    def __init__(self, function_name):
        self.function_name = function_name

    def __str__(self):
        return f"Function {self.function_name} not found"
