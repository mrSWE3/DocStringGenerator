import sys; import os;sys.path.insert(0, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from DocStringGenerator.Construction import add_docstring
if __name__ == "__main__":
    with open("example/a.py") as f, open("example/b.py", "w") as f2:
        f2.writelines(add_docstring(f.readlines()))
