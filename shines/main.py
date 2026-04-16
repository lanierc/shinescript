import sys
from .lexer import Lexer            # Nokta eklendi
from .parser import Parser          # Nokta eklendi
from .interpreter import Interpreter # Nokta eklendi
from . import ast_nodes             # Nokta eklendi

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

# Terminalden 'shines' yazıldığında bu fonksiyon tetiklenecek
def main():
    if len(sys.argv) < 2:
        print("Usage: shines <file.ss>") # python main.py yerine shines yazdık
    else:
        run(sys.argv[1])

if __name__ == '__main__':
    main()
