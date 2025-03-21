import ast

with open("a.py", 'r') as file:
        file_content = file.read()
tree = ast.parse(file_content)
print(([n.lineno for n in ast.walk(tree) if "lineno" in n._attributes]))
print(([i+1 for i,l in enumerate(file_content.split("\n")) if l.strip() != ""]))

ast.