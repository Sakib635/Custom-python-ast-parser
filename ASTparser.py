import ast
import os
import json

class ASTNode:
    def __init__(self, node_type, name=None, value=None, lineno=None, returns=None):
        self.type = node_type
        self.name = name
        self.value = value
        self.lineno = lineno
        self.returns = returns
        self.children = []

    def to_dict(self):
        return {
            "type": self.type,
            "name": self.name,
            "value": self.value,
            "lineno": self.lineno,
            "returns": self.returns,
            "children": [child.to_dict() for child in self.children]
        }

class ASTParser(ast.NodeVisitor):
    def __init__(self):
        self.root = None
        self.current_parent = None

    def visit(self, node):
        node_type = type(node).__name__
        node_info = ASTNode(node_type)

        if isinstance(node, ast.FunctionDef):
            node_info.name = node.name
            node_info.lineno = node.lineno
            if node.returns:
                node_info.returns = self.get_annotation(node.returns)
        elif isinstance(node, ast.arg):
            node_info.name = node.arg
        elif isinstance(node, ast.Name):
            node_info.name = node.id
        elif isinstance(node, ast.Constant):
            node_info.value = node.value
        elif isinstance(node, ast.Expr):
            node_info.lineno = node.lineno

        if self.current_parent is None:
            self.root = node_info
        else:
            self.current_parent.children.append(node_info)

        previous_parent = self.current_parent
        self.current_parent = node_info
        self.generic_visit(node)
        self.current_parent = previous_parent

    def get_annotation(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self.get_annotation(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self.get_annotation(node.value)}[{self.get_annotation(node.slice)}]"
        elif isinstance(node, ast.Index):
            return self.get_annotation(node.value)
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Constant):  # For Python 3.8+
            return node.value
        elif isinstance(node, ast.Tuple):
            return tuple(self.get_annotation(elt) for elt in node.elts)
        return None

    def parse_code(self, code):
        parsed_ast = ast.parse(code)
        self.visit(parsed_ast)
        return self.root

def parse_python_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    
    parser = ASTParser()
    tree_structure = parser.parse_code(code)
    return tree_structure

def save_to_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(data.to_dict(), json_file, indent=4)

if __name__ == "__main__":
    # Provide the path to the Python file you want to parse
   # file_path = "D:/Windsor/Windsor Thesis/AST parser/Codes/snippet1.py"
    file_path ="D:/Windsor/Windsor Thesis/AST parser/Codes/snippet2.py"
    output_path = "output.json"
    
    try:
        tree_structure = parse_python_file(file_path)
        save_to_json(tree_structure, output_path)
        print(f"AST structure saved to {output_path}")
    except FileNotFoundError as e:
        print(e)

