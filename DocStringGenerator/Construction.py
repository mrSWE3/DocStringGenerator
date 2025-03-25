import ast
from .Documentor import GoogleDocumentor,Documentor
from typing import Iterable,List, Tuple

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
                
        if isinstance(node, (ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)) and (over_write_docstrings or not has_docstring(node)):
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

def add_docstring(pre_file: List[str], documentor: Documentor  = GoogleDocumentor(), force:bool = False) -> List[str]:
    doc_strings = ast_doc_string_generator("".join(pre_file), documentor, force)
    doc_strings = sorted(doc_strings,key= lambda t: t[0])
    docstring_len_sum = 0
    for lineno, docstring in doc_strings:
        for ds in docstring[::-1]:
            pre_file.insert(lineno+docstring_len_sum, ds + "\n")
        docstring_len_sum += len(docstring)
    return pre_file





