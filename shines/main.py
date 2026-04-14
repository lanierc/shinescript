import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import ast_nodes

def run(file_path):
    with open(file_path, 'r') as f:
        code = f.read()
        
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        program = parser.parse()
        
        interpreter = Interpreter()
        interpreter.visit(program, interpreter.global_env)
        
        # Automatically call main if it's defined
        if 'main' in interpreter.global_env.functions:
            main_call = ast_nodes.CallFunction('main', [])
            interpreter.visit(main_call, interpreter.global_env)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.ss>")
    else:
        run(sys.argv[1])
