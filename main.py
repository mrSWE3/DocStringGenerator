import ast
from Documentor import GoogleDocumentor,Documentor
from typing import Optional, Iterable
with open('a.py', 'r') as file:
    file_content = file.read()

parsed_ast = ast.parse(file_content)  # Parse the Python file into an AST

def insert_doc_string(node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef, 
                      indent:int,
                      lines: Iterable[str], sep:str="\n"):
    indented_lines = [""] + [("    "*(1+indent // 4)) + l for l in lines] + [""]
    expr = ast.Expr(value =ast.Constant(sep.join(indented_lines)))
    node.body.insert(0,expr)

def ast_doc_string_generator(python_file_path: str, 
                             doc: Documentor, 
                             output_file: Optional[str] = None, 
                             over_write_docstrings: bool=False):
    with open(python_file_path, 'r') as file:
        file_content = file.read()
    tree = ast.parse(file_content)
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)) and not has_docstring(node) or over_write_docstrings:
            if isinstance(node, ast.ClassDef):
                insert_doc_string(node,node.col_offset+1, doc.document_class(node))
            elif isinstance(node, ast.FunctionDef):
                insert_doc_string(node, node.col_offset+1,doc.document_function(node))
            elif isinstance(node, ast.AsyncFunctionDef):
                insert_doc_string(node, node.col_offset+1,doc.document_async_function(node))

    updated_code = ast.unparse(tree)
    if output_file == None:
        output_file = python_file_path
    with open(output_file, "w") as file:
        file.write(updated_code)

def has_docstring(node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Checks if the first statement in a class or function is a valid docstring."""
    if not node.body:
        return False
    
    first_stmt = node.body[0]
    
    return (
        isinstance(first_stmt, ast.Expr) and 
        isinstance(first_stmt.value, ast.Constant) and 
        isinstance(first_stmt.value.value, str)  # Ensure it's a string docstring
    )

if __name__ == "__main__":
    ast_doc_string_generator("a.py", GoogleDocumentor(), "b.py")
    
