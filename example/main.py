import sys; import os;sys.path.insert(0, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from DocStringGenerator.Construction import add_docstring,remove_docstring
if __name__ == "__main__":
    with open("example/a.py") as f:
        a = f.read()
        b = remove_docstring(a)
        lines = add_docstring(b)
    with open("example/b.py", "w") as f:
        f.write(lines)