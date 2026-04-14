class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {}
        self.parent = parent
        
        # Load stdlib if it's the global scope
        if self.parent is None:
            self._init_builtins()
            
    def _init_builtins(self):
        # We store builtins as Python callables
        self.functions['prints'] = self._builtin_prints
        self.functions['inputs'] = self._builtin_inputs
        
    def _builtin_prints(self, args):
        # args is a list of evaluated Python values
        # We can implement string coercion here
        print("".join(str(val) for val in args))
        return None

    def _builtin_inputs(self, args):
        # Wait for user input
        prompt = "".join(str(val) for val in args)
        return input(prompt)
        
    def declare_var(self, name: str, type_name: str, value: any):
        if name in self.variables:
            raise Exception(f"Variable '{name}' already declared in this scope.")
        # Type validation
        self._validate_type(type_name, value)
        self.variables[name] = {'type': type_name, 'value': value}

    def set_var(self, name: str, value: any):
        if name in self.variables:
            type_name = self.variables[name]['type']
            self._validate_type(type_name, value)
            self.variables[name]['value'] = value
            return
            
        if self.parent:
            self.parent.set_var(name, value)
            return
            
        raise Exception(f"Undefined variable '{name}'")
        
    def get_var(self, name: str):
        if name in self.variables:
            return self.variables[name]['value']
            
        if self.parent:
            return self.parent.get_var(name)
            
        raise Exception(f"Undefined variable '{name}'")
        
    def declare_func(self, name: str, node):
        if name in self.functions:
            raise Exception(f"Function '{name}' already declared.")
        self.functions[name] = node
        
    def get_func(self, name: str):
        if name in self.functions:
            return self.functions[name]
            
        if self.parent:
            return self.parent.get_func(name)
            
        raise Exception(f"Undefined function '{name}'")

    def _validate_type(self, type_name: str, value: any):
        # Helper to enforce standard typing
        if type_name == 'int' and not isinstance(value, int):
            raise Exception(f"Type error: expected int, got {type(value).__name__}")
        elif type_name == 'float' and not isinstance(value, float):
            # Sometimes parsing an int into a float variable is acceptable.
            # But let's be strict or implicitly cast.
            if isinstance(value, int):
                value = float(value)
            else:
                raise Exception(f"Type error: expected float, got {type(value).__name__}")
        elif type_name == 'str' and not isinstance(value, str):
            raise Exception(f"Type error: expected str, got {type(value).__name__}")
        elif type_name == 'bool' and not isinstance(value, bool):
            raise Exception(f"Type error: expected bool, got {type(value).__name__}")
