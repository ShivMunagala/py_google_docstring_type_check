#!/usr/bin/env python
"""Check docstrings and type hints in Python files.

Check for consistency between the argument typehints in a function and what the arguments and
typehints given in the function docstring. See README.md for more.
"""
import argparse
from typing import Sequence
import re
import sys


def get_type_hints_from_args(list_of_args: list) -> dict:
    """Extract type hints from a list of function arguments."""
    type_hints = {}
    for param in list_of_args:
        arg, type_hint = param.split(":")
        type_hints[arg] = re.match(r"([\w|\[\]]+)=?", type_hint).group(1)
    return type_hints


def parse_google_docstring(docstring: str) -> dict:
    """Parse Google-style docstring to extract argument names and type."""
    # Extract the "Args:" section from the docstring
    args_section_match = re.search(r"Args:(.*?)(?:\n\n|\Z)", docstring, re.DOTALL)

    if args_section_match:
        args_section = args_section_match.group(1).strip()
        # Parse the "Args:" section to extract argument names and types
        docstring_type_hints = {}
        for line in args_section.split("\n"):
            match = re.match(r"\s*([a-zA-Z0-9_]+) \(([^)]+)\)\s*:\s*([^\n\r]+)", line)
            if match:
                param_name, param_type, _ = match.groups()
                docstring_type_hints[param_name] = param_type.strip()
        return docstring_type_hints
    return {}


def check_args_for_type_hints(args: str) -> dict:
    """
    Check function arguments for the presence of type hints; if yes, return as a dict.

    If one or more args don't have a type hint return an error.

    Args:
        args (str): Arguments for a function as a str.

    Returns:
        dict: Dictionary with keys as arg names and values as arg types.
    """
    if len(args) == 0:
        print("No args to check")
        function_type_hints = {}
    else:
        list_of_args = args.replace(" ", "").split(",")
        list_of_args = [_ for _ in list_of_args if "**" not in _]
        if all(":" in _ for _ in list_of_args):
            function_type_hints = get_type_hints_from_args(list_of_args)
        else:
            print(f"No type hint on one or more args: {args}")
            sys.exit(1)
    return function_type_hints


def single_line_docstring(docstring: str) -> bool:
    """Check if docstring is a single line."""
    return "\n" not in docstring and "\r" not in docstring


def check_docstrings(filename: str) -> None:
    """
    Check that the docstrings of functions in filename are consistent in with the type hints.

    Args:
        filename (str): Path to the file to check.
    """
    try:
        with open(filename, "r", encoding="utf8") as file:
            code = file.read()
    except FileNotFoundError:
        print("Error: No such file or directory: ", filename)
        sys.exit(1)

    if not filename.endswith(".py"):
        print("Error: This hook only accepts '.py' filetypes. You passed: ", filename)
        sys.exit(1)

    # Find all function definitions and their docstrings
    pattern = (
        r"def (\w+)\(([^)]*)\)(?:\s|\n)*(?:->[^:]+)?:[\r\n]+\s*\"\"\"([^\"]*?)\"\"\""
    )
    matches = re.finditer(pattern, code, re.DOTALL)

    for match in matches:
        function_name, args, docstring = match.groups()
        print(f"Checking docstring for function '{function_name}' in {filename}...")

        # Check if the docstring is present
        if not docstring:
            print(f"Error: Function '{function_name}' is missing a docstring.")
            sys.exit(1)

        function_type_hints = check_args_for_type_hints(args)

        # Parse the docstring to extract argument names and types
        docstring_type_hints = parse_google_docstring(docstring)

        # Check the same number of args in function as in docstring
        if len(function_type_hints) != len(
            docstring_type_hints
        ) and not single_line_docstring(docstring):
            print(
                f"There are {len(function_type_hints)} arguments in the function "
                f"{function_name} but {len(docstring_type_hints)} in the docstring."
            )
            sys.exit(1)

        # Compare type hints from the function signature and docstring
        for arg_name, arg_type in function_type_hints.items():
            if arg_name not in docstring_type_hints:
                if single_line_docstring(docstring):
                    print("Single line docstring, nothing to check.")
                else:
                    print(
                        f"Error: Argument '{arg_name}' or its typehint is "
                        f"not in the docstring for function '{function_name}'."
                    )
                    sys.exit(1)
            if (
                arg_name in docstring_type_hints
                and docstring_type_hints[arg_name] != arg_type
            ):
                print(
                    "Error: Type hint mismatch for argument "
                    f"'{arg_name}' in function '{function_name}'."
                )
                sys.exit(1)


def main(argv: Sequence[str] | None = None) -> int:
    """Check typehints of docstring and args of functions in files for consistency."""
    parser = argparse.ArgumentParser(
        description="Check docstrings and type hints in Python files."
    )
    parser.add_argument("filenames", nargs="*", help="List of Python files to check")
    args = parser.parse_args(argv)

    if len(args.filenames) == 0:
        print("No files to check.")
        sys.exit(1)

    for fname in args.filenames:
        check_docstrings(fname)

    sys.exit(0)


if __name__ == "__main__":
    raise SystemExit(main())
