# check_docstrings
### Check docstrings and type hints in Python files.

Check for consistency between ```argument: typehints``` in a function and what the argument typehints given in the Google-style function docstring ```argument (typehint): ...```. Note that the script assumes all functions have docstrings and that all docstrings are in the Google style. Read more about the docstring format at the [Google Python style-guide](https://google.github.io/styleguide/pyguide.html#383-functions-and-methods). You can see more examples of the docstring format [here](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google).

The script can be run as a git hook or with a CLI. Test cases are given in ```tests.py``` and run with ```unittest```. Script is still basic.

Potential improvements:
- Check for return types (-> type)
- Make it optional to not check for arg types, just the args
- Add functionality for different docstring styles (namely reST and Numpydoc)
- Add tests for more complex type hints with combinations of types or nesting, e.g. ```argv: Sequence[str] | None = None```
