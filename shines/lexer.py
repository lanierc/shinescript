import re
from typing import NamedTuple, List

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

class LexerError(Exception):
    def __init__(self, pos: int, line: int, column: int, char: str):
        self.pos = pos
        self.line = line
        self.column = column
        self.char = char
        super().__init__(f"LexerError at line {line}, col {column}: Unexpected character '{char}'")

# Define token patterns
TOKEN_SPECIFICATION = [
    ('FLOAT_LIT',    r'\d+\.\d+'),       # Float literal
    ('INT_LIT',      r'\d+'),            # Integer literal
    ('STR_LIT',      r'"[^"]*"'),        # String literal
    ('BOOL_LIT',     r'\b(true|false)\b'), # Boolean literal
    ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'), # Identifiers
    ('EQ',       r'=='),             # Equal
    ('NEQ',      r'!='),             # Not equal
    ('LEQ',      r'<='),             # Less than or equal
    ('GEQ',      r'>='),             # Greater than or equal
    ('ASSIGN',   r'='),              # Assignment operator
    ('LT',       r'<'),              # Less than
    ('GT',       r'>'),              # Greater than
    ('PLUS',     r'\+'),             # Addition operator
    ('MINUS',    r'-'),              # Subtraction operator
    ('MUL',      r'\*'),             # Multiplication operator
    ('DIV',      r'/'),              # Division operator
    ('LPAREN',   r'\('),             # Left Parenthesis
    ('RPAREN',   r'\)'),             # Right Parenthesis
    ('LBRACE',   r'\{'),             # Left Brace
    ('RBRACE',   r'\}'),             # Right Brace
    ('SEMI',     r';'),              # Statement terminator
    ('COMMA',    r','),              # Comma separator
    ('NEWLINE',  r'\n'),             # Line endings
    ('SKIP',     r'[ \t]+'),         # Skip over spaces and tabs
    ('COMMENT',  r'//[^\n]*'),       # Comments
    ('MISMATCH', r'.'),              # Any other character
]

KEYWORDS = {
    'int', 'float', 'str', 'bool',
    'func', 'if', 'else', 'while', 'return'
}

class Lexer:
    def __init__(self, code: str):
        self.code = code
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
        self.get_token = re.compile(tok_regex).match
        self.line_num = 1
        self.line_start = 0
        self.pos = 0

    def tokenize(self) -> List[Token]:
        tokens = []
        mo = self.get_token(self.code, self.pos)
        while mo is not None:
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == 'NEWLINE':
                self.line_start = mo.end()
                self.line_num += 1
            elif kind == 'SKIP' or kind == 'COMMENT':
                pass
            elif kind == 'MISMATCH':
                raise LexerError(self.pos, self.line_num, mo.start() - self.line_start + 1, value)
            else:
                if kind == 'ID' and value in KEYWORDS:
                    kind = value.upper()
                column = mo.start() - self.line_start + 1
                
                # String literals should have their quotes stripped inside the value
                if kind == 'STR_LIT':
                    value = value[1:-1]
                    
                tokens.append(Token(kind, value, self.line_num, column))
            self.pos = mo.end()
            mo = self.get_token(self.code, self.pos)
            
        tokens.append(Token('EOF', 'EOF', self.line_num, self.pos - self.line_start + 1))
        return tokens
