from typing import List, Optional
from .lexer import Token
from . import ast_nodes

class ParserError(Exception):
    def __init__(self, token: Token, message: str):
        super().__init__(f"ParserError at line {token.line}, col {token.column}: {message}")

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def eat(self, token_type: str) -> Token:
        token = self.current_token()
        if token.type == token_type:
            self.pos += 1
            return token
        raise ParserError(token, f"Expected {token_type}, got {token.type} ('{token.value}')")

    def parse(self) -> ast_nodes.Program:
        statements = []
        while self.current_token().type != 'EOF':
            statements.append(self.parse_statement())
        return ast_nodes.Program(statements)

    def parse_statement(self) -> ast_nodes.AST:
        token = self.current_token()
        
        if token.type in ('INT', 'FLOAT', 'STR', 'BOOL'):
            return self.parse_variable_declaration()
            
        elif token.type == 'FUNC':
            return self.parse_function_declaration()
            
        elif token.type == 'IF':
            return self.parse_if_statement()
            
        elif token.type == 'WHILE':
            return self.parse_while_loop()
        elif token.type == 'FOR': # YENİ EKLENEN KISIM
            return self.parse_for_loop()
        elif token.type == 'RETURN':
            return self.parse_return_statement()
            
        elif token.type == 'ID':
            # Could be assignment or function call statement
            # Look ahead to see if it's an assignment
            next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if next_token and next_token.type == 'ASSIGN':
                return self.parse_assignment()
        
        # If it's none of the specific statement structures, parse as an expression statement
        expr = self.parse_expression()
        self.eat('SEMI')
        return expr

    def parse_variable_declaration(self) -> ast_nodes.AST:
        type_token = self.current_token()
        self.eat(type_token.type) # e.g. INT, STR
        
        var_name_token = self.eat('ID')
        self.eat('ASSIGN')
        
        value = self.parse_expression()
        self.eat('SEMI')
        
        return ast_nodes.VariableDeclaration(type_token.value, var_name_token.value, value)

    def parse_assignment(self, require_semi: bool = True) -> ast_nodes.AST:
        var_name_token = self.eat('ID')
        
        token = self.current_token()
        if token.type == 'ASSIGN':
            self.eat('ASSIGN')
            value = self.parse_expression()
            
        elif token.type in ('PLUS_ASSIGN', 'MINUS_ASSIGN'):
            op_token = self.eat(token.type)
            op = '+' if op_token.type == 'PLUS_ASSIGN' else '-'
            right_value = self.parse_expression()
            
            # Arka planda x += 5'i -> x = x + 5'e dönüştürüyoruz
            value = ast_nodes.BinaryOperation(
                ast_nodes.Identifier(var_name_token.value),
                op,
                right_value
            )
        else:
            raise ParserError(token, f"Expected '=', '+=' or '-=', got {token.type}")
            
        if require_semi:
            self.eat('SEMI')
            
        return ast_nodes.Assignment(var_name_token.value, value)
        
    def parse_for_loop(self) -> ast_nodes.AST:
        self.eat('FOR')
        self.eat('LPAREN')
        
        # 1. Başlangıç ataması (Örn: int i = 0; veya i = 0;)
        init_node = None
        if self.current_token().type in ('INT', 'FLOAT', 'STR', 'BOOL'):
            init_node = self.parse_variable_declaration() # Zaten SEMI yutuyor
        elif self.current_token().type == 'ID':
            init_node = self.parse_assignment() # Zaten SEMI yutuyor
        else:
            self.eat('SEMI') # Boş geçilmişse (Örn: for(; i<10; ...))
            
        # 2. Koşul (Örn: i < 10)
        condition = None
        if self.current_token().type != 'SEMI':
            condition = self.parse_expression()
        self.eat('SEMI')
        
        # 3. Güncelleme/Artırım (Örn: i = i + 1)
        update_node = None
        if self.current_token().type == 'ID':
            # Noktalı virgül beklememesi için require_semi=False diyoruz
            update_node = self.parse_assignment(require_semi=False) 
            
        self.eat('RPAREN')
        
        # 4. Gövde
        body = self.parse_block()
        
        return ast_nodes.ForLoop(init_node, condition, update_node, body)
        
    def parse_function_declaration(self) -> ast_nodes.AST:
        self.eat('FUNC')
        name_token = self.eat('ID')
        self.eat('LPAREN')
        
        params = []
        if self.current_token().type != 'RPAREN':
            while True:
                type_token = self.current_token()
                if type_token.type not in ('INT', 'FLOAT', 'STR', 'BOOL'):
                    raise ParserError(type_token, f"Expected type name, got {type_token.type}")
                self.eat(type_token.type)
                param_name = self.eat('ID').value
                params.append({'name': param_name, 'type': type_token.value})
                
                if self.current_token().type == 'COMMA':
                    self.eat('COMMA')
                else:
                    break
                    
        self.eat('RPAREN')
        body = self.parse_block()
        
        return ast_nodes.FunctionDeclaration(name_token.value, params, body)

    def parse_if_statement(self) -> ast_nodes.AST:
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.parse_expression()
        self.eat('RPAREN')
        
        true_body = self.parse_block()
        false_body = None
        
        if self.current_token().type == 'ELSE':
            self.eat('ELSE')
            false_body = self.parse_block()
            
        return ast_nodes.IfStatement(condition, true_body, false_body)

    def parse_while_loop(self) -> ast_nodes.AST:
        self.eat('WHILE')
        self.eat('LPAREN')
        condition = self.parse_expression()
        self.eat('RPAREN')
        
        body = self.parse_block()
        return ast_nodes.WhileLoop(condition, body)

    def parse_return_statement(self) -> ast_nodes.AST:
        self.eat('RETURN')
        if self.current_token().type == 'SEMI':
            self.eat('SEMI')
            return ast_nodes.ReturnStatement(None)
        
        value = self.parse_expression()
        self.eat('SEMI')
        return ast_nodes.ReturnStatement(value)

    def parse_block(self) -> List[ast_nodes.AST]:
        self.eat('LBRACE')
        statements = []
        while self.current_token().type not in ('RBRACE', 'EOF'):
            statements.append(self.parse_statement())
        self.eat('RBRACE')
        return statements

    def parse_expression(self) -> ast_nodes.AST:
        return self.parse_equality()

    def parse_equality(self) -> ast_nodes.AST:
        node = self.parse_comparison()
        
        while self.current_token().type in ('EQ', 'NEQ'):
            op_token = self.current_token()
            self.eat(op_token.type)
            node = ast_nodes.BinaryOp(left=node, op=op_token.type, right=self.parse_comparison())
            
        return node

    def parse_comparison(self) -> ast_nodes.AST:
        node = self.parse_term()
        
        while self.current_token().type in ('LT', 'GT', 'LEQ', 'GEQ'):
            op_token = self.current_token()
            self.eat(op_token.type)
            node = ast_nodes.BinaryOp(left=node, op=op_token.type, right=self.parse_term())
            
        return node

    def parse_term(self) -> ast_nodes.AST:
        node = self.parse_factor()
        
        while self.current_token().type in ('PLUS', 'MINUS'):
            op_token = self.current_token()
            self.eat(op_token.type)
            node = ast_nodes.BinaryOp(left=node, op=op_token.type, right=self.parse_factor())
            
        return node

    def parse_factor(self) -> ast_nodes.AST:
        node = self.parse_primary()
        
        while self.current_token().type in ('MUL', 'DIV'):
            op_token = self.current_token()
            self.eat(op_token.type)
            node = ast_nodes.BinaryOp(left=node, op=op_token.type, right=self.parse_primary())
            
        return node

    def parse_primary(self) -> ast_nodes.AST:
        token = self.current_token()
        
        if token.type == 'INT_LIT':
            self.eat('INT_LIT')
            return ast_nodes.Literal('int', int(token.value))
            
        elif token.type == 'FLOAT_LIT':
            self.eat('FLOAT_LIT')
            return ast_nodes.Literal('float', float(token.value))
            
        elif token.type == 'STR_LIT':
            self.eat('STR_LIT')
            return ast_nodes.Literal('str', token.value)
            
        elif token.type == 'BOOL_LIT':
            self.eat('BOOL_LIT')
            return ast_nodes.Literal('bool', token.value == 'true')
            
        elif token.type == 'ID':
            self.eat('ID')
            # Check if it's a function call
            if self.current_token().type == 'LPAREN':
                self.eat('LPAREN')
                args = []
                if self.current_token().type != 'RPAREN':
                    while True:
                        args.append(self.parse_expression())
                        if self.current_token().type == 'COMMA':
                            self.eat('COMMA')
                        else:
                            break
                self.eat('RPAREN')
                return ast_nodes.CallFunction(token.value, args)
            else:
                return ast_nodes.Identifier(token.value)
                
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.parse_expression()
            self.eat('RPAREN')
            return node
        elif token.type == 'LBRACK':
            self.eat('LBRACK')
            elements = []
            if self.current_token().type != 'RBRACK':
                while True:
                    elements.append(self.parse_expression())
                    if self.current_token().type == 'COMMA':
                        self.eat('COMMA')
                    else:
                        break
            self.eat('RBRACK')
            return ast_nodes.ArrayLiteral(elements)
        
        raise ParserError(token, f"Unexpected token in expression: {token.type} ('{token.value}')")
