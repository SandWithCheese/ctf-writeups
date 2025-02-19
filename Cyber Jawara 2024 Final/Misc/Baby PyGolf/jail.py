#!/usr/local/bin/python3 -S
from ast import parse
from ast import NodeVisitor

BANNED = '012345678}!<%[$/#{+`*;~>\'\\&-(]=|"^?,)'

class Node(NodeVisitor):
    def visit_Attribute(self, node):
        assert "_" in node.attr, ":x"
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        assert "_" in node.name, ":x"
        self.generic_visit(node)

def run_code(code):
    for char in set(code):
        assert char not in BANNED, ':x'
    assert code.__len__() < 145

    tree = parse(code)
    Node().visit(tree)

    __builtins__.__dict__.clear()
    
    safe_builtins = {'__build_class__': err}
    e(code, {'__builtins__': safe_builtins})

i, e, err = input, exec, RuntimeError
user_input = i('>>> ')

try:
    run_code(user_input)
except:
    pass
