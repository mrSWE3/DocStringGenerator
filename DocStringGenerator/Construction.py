import ast
from .Documentor import GoogleDocumentor,Documentor
from typing import Iterable,List, Optional, Dict

def insert_doc_string(indent:int,
                      lines: Iterable[str], 
                      sep:str="\n") -> List[str]:
    indented_lines = [("    "*(1+indent // 4)) + l for l in ["\"\"\""] + list(lines) + ["\"\"\""]]
    return indented_lines

def ast_doc_string_generator(python_lines: str, 
                             doc: Documentor, 
                             over_write_docstrings: bool=False
                             ) -> Dict[int, List[str]]:
    tree = ast.parse(python_lines)
    docstring_lineno: Dict[int, List[str]] = {}
    
    for node in ast.walk(tree):
        
        if isinstance(node, (ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)) and (over_write_docstrings or not has_docstring(node)):
            if isinstance(node, ast.ClassDef):
                docstring = insert_doc_string(node.col_offset+1, doc.document_class(node))
                docstring_lineno[node.body[0].lineno] = docstring
            elif isinstance(node, ast.FunctionDef):
                docstring = insert_doc_string(node.col_offset+1,doc.document_function(node))
                docstring_lineno[node.body[0].lineno] = docstring
            else:
                docstring = insert_doc_string(node.col_offset+1,doc.document_async_function(node))
                docstring_lineno[node.body[0].lineno] = docstring

    return docstring_lineno
 
def remove_docstring(python_file: str) -> str:
    tree = ast.parse(python_file)
    docstring_lineno: List[int] = [0]
    for node in ast.walk(tree):
        docstring = get_docstring(node)
        if  docstring != None:
            docstring_lineno.append(docstring.lineno-1)
            docstring_lineno.append((docstring.end_lineno if docstring.end_lineno else docstring.lineno))
    docstring_lineno.append(tree.body[-1].end_lineno if tree.body[-1].end_lineno else tree.body[-1].lineno)
    docstring_lineno = sorted(docstring_lineno)
    slices =  zip(docstring_lineno[:-1][::2],docstring_lineno[1:][::2])
    final_lines:List[str] = []
    python_lines = python_file.split("\n")
  
    for s in slices:
        final_lines.extend(python_lines[s[0]:s[1]])
        
    return "\n".join(final_lines) + "\n"
def get_docstring(node: ast.AST) -> Optional[ast.Constant]:
    """Checks if the first statement in a class or function is a valid docstring."""
    if not isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return None
    if not node.body:
        return None
    
    first_stmt = node.body[0]
    
    if (isinstance(first_stmt, ast.Expr) and 
        isinstance(first_stmt.value, ast.Constant) and 
        isinstance(first_stmt.value.value, str)):
        return first_stmt.value
    elif isinstance(first_stmt, ast.Constant):
        if isinstance(first_stmt.value, str):
            return first_stmt
    return None

def has_docstring(node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Checks if the first statement in a class or function is a valid docstring."""
    return get_docstring(node) != None

def add_docstring(file: str, documentor: Documentor  = GoogleDocumentor()) -> str:

    line_operations = ast_doc_string_generator(file, documentor)
    pre_file = [l + "\n" for l in file.split("\n")]
    docstring_len_sum = 0
    for lineno,  doc_string in sorted(line_operations.items()):
        empty_above = 0
        tmp = lineno-1-empty_above-1 + docstring_len_sum
        if  pre_file[tmp].strip() == "":
            while pre_file[tmp].strip() == "":
                tmp = lineno-1-empty_above-1 + docstring_len_sum
                empty_above += 1
            empty_above -= 1

        for ds in [""] + doc_string[::-1]:
            pre_file.insert(lineno-1+docstring_len_sum-empty_above, ds + "\n")
        docstring_len_sum += len(doc_string) + 1
    return "".join(pre_file)





