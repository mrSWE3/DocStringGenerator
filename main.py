import ast
from Documentor import GoogleDocumentor,Documentor
from typing import Optional, Iterable,List, Tuple
with open('a.py', 'r') as file:
    file_content = file.read()

parsed_ast = ast.parse(file_content)  # Parse the Python file into an AST

def insert_doc_string(indent:int,
                      lines: Iterable[str], 
                      sep:str="\n") -> List[str]:
    
    indented_lines = [("    "*(1+indent // 4)) + l for l in ["\"\"\""] + list(lines) + ["\"\"\""]]
    return indented_lines

def ast_doc_string_generator(python_lines: str, 
                             doc: Documentor, 
                             over_write_docstrings: bool=False) -> List[Tuple[int, List[str]]]:
    tree = ast.parse(python_lines)
    docstring_lineno: List[Tuple[int, List[str]]] = []
    for node in ast.walk(tree):
                
        if isinstance(node, (ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)) and not has_docstring(node) or over_write_docstrings:
            if isinstance(node, ast.ClassDef):
                docstring = insert_doc_string(node.col_offset+1, doc.document_class(node))
                docstring_lineno.append((node.lineno, docstring))
            elif isinstance(node, ast.FunctionDef):
                docstring = insert_doc_string(node.col_offset+1,doc.document_function(node))
                docstring_lineno.append((node.lineno, docstring))
            elif isinstance(node, ast.AsyncFunctionDef):
                docstring = insert_doc_string(node.col_offset+1,doc.document_async_function(node))
                docstring_lineno.append((node.lineno, docstring))

    return docstring_lineno

def ast_doc_string_generator_keep_empty_spaces(python_lines: List[str], 
                             doc: Documentor, 
                             over_write_docstrings: bool=False) -> str:
    line_groups: List[str] = []
    i = 0
    while i < len(python_lines): 
        if python_lines[i].strip() == "":
            line_groups.append(python_lines[i])
            i += 1
        else:
            current_group:List[str] = []
            while i < len(python_lines) and not python_lines[i].strip() == "":
                current_group.append(python_lines[i])
                i += 1
            line_groups.append(ast_doc_string_generator("".join(current_group), doc, over_write_docstrings))
    return "".join(line_groups)



        

    
    

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
    with open("a.py","r") as f:
        original_file = f.readlines()
        new_file = ast_doc_string_generator("".join(original_file), GoogleDocumentor())
    
    docstring_len_sum = 0
    for lineno, docstring in new_file:
        for ds in docstring[::-1]:
            original_file.insert(lineno+docstring_len_sum, ds + "\n")
        docstring_len_sum += len(docstring)
    print("".join(original_file))
