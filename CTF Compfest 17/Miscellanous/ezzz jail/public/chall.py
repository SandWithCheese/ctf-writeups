#!/usr/bin/env python3
import base64
from RestrictedPython import compile_restricted, safe_globals
from safe_exceptions import EXCEPTIONS_TO_REMOVE  

error = RuntimeError('error')
_original_safe_globals = None

def get_globals():
    global _original_safe_globals
    
    if _original_safe_globals is None:
        safe_globals_copy = safe_globals.copy()
        
        for exc in EXCEPTIONS_TO_REMOVE:
            if exc in safe_globals_copy['__builtins__']:
                del safe_globals_copy['__builtins__'][exc]
        
        safe_globals_copy['__builtins__']['error'] = error
        safe_globals_copy['__builtins__']['open'] = open
        
        _original_safe_globals = safe_globals_copy
    
    return _original_safe_globals

def run_code(code):
    try:
        bytecode = compile_restricted(code, '<input>', 'exec')
        if bytecode is None:
            return
        exec(bytecode, get_globals())
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        try:
            code = input(">>> ")
            if code == "exit":
                break
            if code.startswith("b64:"):
                code = base64.b64decode(code[4:]).decode()
            run_code(code)
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    main()