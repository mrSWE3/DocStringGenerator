from typing import Protocol, Iterable, List, Type, Set
import ast

class Documentor(Protocol):
    def document_class(self, class_def: ast.ClassDef) -> Iterable[str]:
        ...
    def document_function(self, func_def: ast.FunctionDef) -> Iterable[str]:
        ...
    def document_async_function(self, func_def: ast.AsyncFunctionDef) -> Iterable[str]:
        ...


def extract_from_function[T: ast.AST](func: ast.FunctionDef | ast.AsyncFunctionDef, stmt_type: Type[T]) -> List[T]:
    # Parse the code into an AST
    # List to hold raise statements in the target function
    raise_statements: List[T] = []
    target_function = func.name
    # Traverse all function definitions
    for node in ast.walk(func):
        if isinstance(node, ast.FunctionDef):
            # If the current function is the one we're targeting
            if node.name == target_function:
                # Walk through the body of the target function
                for stmt in node.body:
                    if isinstance(stmt, stmt_type):  # Look for raise statements
                        stmt.lineno
                        raise_statements.append(stmt)  # Convert to source code
    return raise_statements
                        
def add_section(header:str, current_lines: List[str], new_lines: List[str]):
    if len(new_lines) == 0:
        return
    current_lines.append(header)
    current_lines.extend(["    " + l for l in new_lines])

class FillInDocumentor(Documentor, Protocol):
    def document_class(self, class_def: ast.ClassDef) -> Iterable[str]:
        lines: List[str] = []
        add_section("## Summary", lines, [""])
        add_section("## Decorators", lines, self.document_decorators(class_def.decorator_list))
        add_section("## Type Params", lines, self.document_type_params(class_def.type_params))
        add_section("## Key Words", lines, self.document_key_words(class_def.keywords))
        lines.append("")
        return lines
    def document_function(self, func_def: ast.FunctionDef) -> Iterable[str]:
        lines: List[str] = []
        add_section("## Summary", lines, [""])
        add_section("## Type params", lines, self.document_type_params(func_def.type_params))
        add_section("## Args", lines, self.document_args(func_def.args))
        add_section("## Exceptions", lines, self.document_raises(extract_from_function(func_def, ast.Raise)))
        add_section("## Yields", lines, self.document_yields(func_def.returns))
        add_section("## Return", lines, self.document_returns(func_def.returns))
        lines.append("")
        return lines
    def document_async_function(self, func_def: ast.AsyncFunctionDef) -> Iterable[str]:
        lines: List[str] = []
        add_section("## Summary", lines, [""])
        add_section("## Type params", lines, self.document_type_params(func_def.type_params))
        add_section("## Args", lines, self.document_args(func_def.args))
        add_section("## Exceptions", lines, self.document_raises(extract_from_function(func_def, ast.Raise)))
        add_section("## Yields", lines, self.document_yields(func_def.returns))
        add_section("## Return", lines, self.document_returns(func_def.returns))
        lines.append("")
        return lines

    def document_key_words(self, key_words: List[ast.keyword]) -> List[str]:
        ...
    def document_decorators(self, decorators: List[ast.expr]) -> List[str]:
        ...
    def document_type_params(self, type_params: List[ast.type_param]) -> List[str]:
        ...
    def document_args(self, args: ast.arguments)->List[str]:
        ...
    def document_raises(self, raises: List[ast.Raise])->List[str]:
        ...
    def document_yields(self, returns_type: ast.expr | None)->List[str]:
        ...
    def document_returns(self, returns_type: ast.expr | None)->List[str]:
        ...

class GoogleDocumentor(FillInDocumentor):
    def document_key_words(self, key_words: List[ast.keyword]) -> List[str]:
        return []
    def document_decorators(self, decorators: List[ast.expr]) -> List[str]:
        return []
    def document_type_params(self, type_params: List[ast.type_param]) -> List[str]:
        lines: List[str] = []
        for tp in type_params:
            
            if isinstance(tp, ast.TypeVar):
                    
                bound : ast.expr | None = tp.bound
                name: str = tp.name
                bound_Str = ""
                
                if not bound == None:
                    bound_Str = f" ({ast.unparse(bound)})"


                lines.append(f"{name}{bound_Str}: ")
                    
                    
            elif  isinstance(tp, ast.TypeVarTuple):
                lines.append(f"{tp.name}: ")
            elif isinstance(tp, ast.ParamSpec):
                lines.append(f"{tp.name}: ")
            else:
                raise Exception("Should not be here?", ast.dump(tp))
        return lines

    def document_args(self, args: ast.arguments)->List[str]:
        return [f"{arg.arg}{"" if arg.annotation == None else f" ({ast.unparse(arg.annotation)})"}: " for i,arg in enumerate(args.args + 
                [vararg for vararg in [args.vararg] if vararg != None]+
                [kwarg for kwarg in [args.kwarg] if kwarg != None]) if i!=0 or arg.arg != "self"]
            
    def document_raises(self, raises: List[ast.Raise])->List[str]:
        lines: Set[str] = set()
        for raise_stmt in raises:
            if isinstance(raise_stmt.exc, ast.Call) and isinstance(raise_stmt.exc.func, ast.Name):
                lines.add(f"{raise_stmt.exc.func.id}")
            else:
                lines.add(str(ast.unparse(raise_stmt.exc) if raise_stmt.exc != None else None))
        return list(lines)
    def document_yields(self, returns_type: ast.expr | None)->List[str]:
        lines: List[str] = []
        if isinstance(returns_type, ast.Subscript
                      ) and isinstance(returns_type.value, ast.Name
                                       ) and returns_type.value.id == "Generator":
            if isinstance(returns_type.slice, ast.Name):
                lines.append(returns_type.slice.id)
            elif isinstance(returns_type.slice, ast.Tuple):
                lines.append(ast.unparse(returns_type.slice.elts[0]))
            else:
                raise Exception(f"Not supposed to be here {ast.dump(returns_type.slice)}")
        return lines

            
    def document_returns(self, returns_type: ast.expr | None)->List[str]:
        if returns_type != None and ast.unparse(returns_type) != "None":
            return [f"{ast.unparse(returns_type)}"]
        return []


