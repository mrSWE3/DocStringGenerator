import ast

with open("a.py", 'r') as file:
        file_content = file.read()
tree = ast.parse(file_content)
print(ast.dump  ((tree)))