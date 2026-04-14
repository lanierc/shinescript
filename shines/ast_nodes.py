from typing import List, Optional

class AST:
    pass

class Program(AST):
    def __init__(self, statements: List[AST]):
        self.statements = statements

class FunctionDeclaration(AST):
    def __init__(self, name: str, params: List[dict], body: List[AST]):
        # params is a list of dicts: [{'name': 'x', 'type': 'int'}]
        self.name = name
        self.params = params
        self.body = body

class IfStatement(AST):
    def __init__(self, condition: AST, true_body: List[AST], false_body: Optional[List[AST]]):
        self.condition = condition
        self.true_body = true_body
        self.false_body = false_body

class WhileLoop(AST):
    def __init__(self, condition: AST, body: List[AST]):
        self.condition = condition
        self.body = body

class VariableDeclaration(AST):
    def __init__(self, type_name: str, var_name: str, value: AST):
        self.type_name = type_name
        self.var_name = var_name
        self.value = value

class Assignment(AST):
    def __init__(self, var_name: str, value: AST):
        self.var_name = var_name
        self.value = value

class ReturnStatement(AST):
    def __init__(self, value: Optional[AST]):
        self.value = value

class BinaryOp(AST):
    def __init__(self, left: AST, op: str, right: AST):
        self.left = left
        self.op = op
        self.right = right

class Literal(AST):
    def __init__(self, type_name: str, value: any):
        # type_name should be 'int', 'float', 'str', or 'bool'
        self.type_name = type_name
        self.value = value

class Identifier(AST):
    def __init__(self, name: str):
        self.name = name

class CallFunction(AST):
    def __init__(self, name: str, args: List[AST]):
        self.name = name
        self.args = args
