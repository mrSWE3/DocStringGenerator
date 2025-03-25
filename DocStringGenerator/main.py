import argparse
from DocStringGenerator.Construction import add_docstring,remove_docstring

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="A command-line tool for generating docstrings.")
    
    # Input file argument (positional argument)
    parser.add_argument(
        'input', 
        type=str, 
        help="The Python file to generate docstrings for"
    )
    
    # Output file argument (optional argument)
    parser.add_argument(
        '-o', '--output',
        type=str, 
        help="Output destination for input file with docstrings added"
    )
    
    parser.add_argument(
        '-f', '--force', 
        action='store_true', 
        help="Add new docstring even if one already exists"
    )

    
    # Parse the arguments
    args = parser.parse_args()
    
    # Get input and output file names from the parsed arguments
    in_py = args.input  # Correct access to the input file
    out_py = args.output if args.output else in_py  # Use in_py as default for out_py
    
    # Open input and output files
    with open(in_py) as f:
        # Call add_docstring and write the result to the output file
        file_text = f.read()
        if bool(args.force):
            file_text = remove_docstring(file_text)
        lines = add_docstring(file_text)
    with open(out_py, "w") as f:
        f.writelines(lines)
if __name__ == "__main__":
    main()
