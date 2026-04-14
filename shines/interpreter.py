import ast_nodes
from environment import Environment

class Interpreter:
    def __init__(self):
        self.global_env = Environment()

    def visit(self, node, env: Environment):
        if hasattr(self, f'visit_{type(node).__name__}'):
            method = getattr(self, f'visit_{type(node).__name__}')
            return method(node, env)
        raise Exception(f"No visit method for node type {type(node).__name__}")

    def visit_Program(self, node: ast_nodes.Program, env: Environment):
        for stmt in node.statements:
            self.visit(stmt, env)

    def visit_VariableDeclaration(self, node: ast_nodes.VariableDeclaration, env: Environment):
        value = self.visit(node.value, env)
        env.declare_var(node.var_name, node.type_name, value)

    def visit_Assignment(self, node: ast_nodes.Assignment, env: Environment):
        value = self.visit(node.value, env)
        env.set_var(node.var_name, value)

    def visit_FunctionDeclaration(self, node: ast_nodes.FunctionDeclaration, env: Environment):
        env.declare_func(node.name, node)

    def visit_IfStatement(self, node: ast_nodes.IfStatement, env: Environment):
        condition = self.visit(node.condition, env)
        if condition:
            # Create a new block scope
            block_env = Environment(env)
            for stmt in node.true_body:
                result = self.visit(stmt, block_env)
                if isinstance(result, ReturnValue):
                    return result
        elif node.false_body:
            block_env = Environment(env)
            for stmt in node.false_body:
                result = self.visit(stmt, block_env)
                if isinstance(result, ReturnValue):
                    return result

    def visit_WhileLoop(self, node: ast_nodes.WhileLoop, env: Environment):
        while self.visit(node.condition, env):
            block_env = Environment(env)
            for stmt in node.body:
                result = self.visit(stmt, block_env)
                if isinstance(result, ReturnValue):
                    return result

    def visit_ReturnStatement(self, node: ast_nodes.ReturnStatement, env: Environment):
        value = None
        if node.value is not None:
            value = self.visit(node.value, env)
        return ReturnValue(value)

    def visit_BinaryOp(self, node: ast_nodes.BinaryOp, env: Environment):
        left = self.visit(node.left, env)
        right = self.visit(node.right, env)

        if node.op == 'PLUS': return left + right
        if node.op == 'MINUS': return left - right
        if node.op == 'MUL': return left * right
        if node.op == 'DIV': return left / right
        if node.op == 'EQ': return left == right
        if node.op == 'NEQ': return left != right
        if node.op == 'LT': return left < right
        if node.op == 'GT': return left > right
        if node.op == 'LEQ': return left <= right
        if node.op == 'GEQ': return left >= right

        raise Exception(f"Unknown operator {node.op}")

    def visit_Literal(self, node: ast_nodes.Literal, env: Environment):
        return node.value

    def visit_Identifier(self, node: ast_nodes.Identifier, env: Environment):
        return env.get_var(node.name)

    def visit_CallFunction(self, node: ast_nodes.CallFunction, env: Environment):
        func = env.get_func(node.name)
        args_eval = [self.visit(arg, env) for arg in node.args]

        if callable(func):
            # Built-in function like prints or inputs
            return func(args_eval)
        else:
            # User defined function
            if len(args_eval) != len(func.params):
                raise Exception(f"Function {node.name} expects {len(func.params)} arguments")
                
            func_env = Environment(self.global_env) # functions use lexical scope from global
            for param, arg_val in zip(func.params, args_eval):
                func_env.declare_var(param['name'], param['type'], arg_val)

            for stmt in func.body:
                result = self.visit(stmt, func_env)
                if isinstance(result, ReturnValue):
                    return result.value
            return None

class ReturnValue:
    """Wrapper to signal a return out of a block"""
    def __init__(self, value):
        self.value = value
