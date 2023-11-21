"""Tests for check_docstrings.py using unittest."""
import os
import unittest
from check_docstrings import main


class TestCheckDocstrings(unittest.TestCase):
    """Test class for check_docstrings."""

    def write_str_and_assert_exception(self, file_content, code):
        """Write file_content to a file and check that main() raises code."""
        file = "test_file.py"
        with open(file, "w", encoding="utf-8") as f:
            f.write(file_content)

        try:
            with self.assertRaises(SystemExit) as cm:
                main([file])
            self.assertEqual(cm.exception.code, code)
        finally:
            os.remove(file)  # Clean up: remove the temporary file

    def test_nonexistent_file(self):
        with self.assertRaises(SystemExit) as cm:
            main(["nonexistent_file.py"])
        self.assertEqual(cm.exception.code, 1)

    def test_single_line_docstring(self):
        self.write_str_and_assert_exception(
            (
                "def single_line_docstring(a: int) -> None:\n"
                '    """Single line."""\n'
                "    return\n"
            ),
            0,
        )

    def test_working_no_args(self):
        self.write_str_and_assert_exception(
            (
                "def working_no_args() -> None:\n"
                '   """\n'
                "   Zero arguments.\n"
                '   """\n'
                "   return\n"
            ),
            0,
        )


    def test_working_multiline_docstring_arg(self):
        self.write_str_and_assert_exception(
            (
                "def working_multi_line(a: int, b: str) -> None:\n"
                '   """\n'
                "   Multiline for arg a.\n"
                "\n"
                "   Args:\n"
                "       a (int): This is a\n"
                "           multi-line description of arg a.\n"
                "       b (str): This is also a\n"
                "           multi-line description.\n"
                '   """\n'
                "   return\n"
            ),
            0,
        )

    def test_one_mismatch_arg(self):
        self.write_str_and_assert_exception(
            (
                "def one_mismatch_arg(a: int) -> None:\n"
                '   """\n'
                "   One argument.\n"
                "\n"
                "   Args:\n"
                "       a (str): Integer.\n"
                '   """\n'
                "   return\n"
            ),
            1,
        )


    def test_with_default_arg(self):
        self.write_str_and_assert_exception(
            (
                "def one_mismatch_arg(a: int = 5) -> None:\n"
                '   """\n'
                "   One argument.\n"
                "\n"
                "   Args:\n"
                "       a (int): Integer. Default 5.\n"
                '   """\n'
                "   return\n"
            ),
            0,
        )

    def test_arg_not_in_docstring_args(self):
        self.write_str_and_assert_exception(
            (
                "def arg_not_in_docstring_args(a: int) -> None:\n"
                '   """\n'
                "   One argument\n"
                "\n"
                "   Args:\n"
                "       b (int): Integer.\n"
                '   """\n'
                "   return\n"
            ),
            1,
        )

    def test_extra_arg_in_docstring(self):
        self.write_str_and_assert_exception(
            (
                "def exta_arg_in_docstring(a: int) -> None:\n"
                '   """\n'
                "   One argument\n"
                "\n"
                "   Args:\n"
                "       a (int): Integer.\n"
                "       b (int): Integer.\n"
                '   """\n'
                "   return\n"
            ),
            1,
        )

    def test_multiple_mismatch_args(self):
        self.write_str_and_assert_exception(
            (
                "def multiple_mismatch_arg(a: float, b: int, c: str) -> None:\n"
                '   """\n'
                "   One argument\n"
                "\n"
                "   Args:\n"
                "        a (int): Integer.\n"
                "        b (float): Float.\n"
                "        c (str): str.\n"
                '    """\n'
                "    return\n"
            ),
            1,
        )

    def test_empty_type_in_docstring(self):
        self.write_str_and_assert_exception(
            (
                "def empty_type_in_docstring(a: int) -> None:\n"
                '    """\n'
                "    One argument\n"
                "\n"
                "    Args:\n"
                "        a (): Integer.\n"
                '    """\n'
                "    return\n"
            ),
            1,
        )

    def test_no_type_in_docstring(self):
        self.write_str_and_assert_exception(
            (
                "def no_type_in_docstring(a: int) -> None:\n"
                '    """\n'
                "    One argument\n"
                "\n"
                "    Args:\n"
                "        a: Integer.\n"
                '    """\n'
                "    return\n"
            ),
            1,
        )

    def test_no_args_in_docstring(self):
        self.write_str_and_assert_exception(
            (
                "def no_args_in_docstring(a: int) -> None:\n"
                '    """\n'
                "    One argument.\n"
                '    """\n'
                "    return\n"
            ),
            1,
        )

    def test_no_typehint(self):
        self.write_str_and_assert_exception(
            (
                "def no_typehint(a) -> None:\n"
                '    """\n'
                "    One argument\n"
                "\n"
                "    Args:\n"
                "        a (int): Integer.\n"
                '    """\n'
                "    return\n"
            ),
            1,
        )

    def test_working_one_arg(self):
        self.write_str_and_assert_exception(
            (
                "def one_arg(arg: int) -> None:\n"
                '    """\n'
                "    One argument.\n"
                "\n"
                "    Args:\n"
                "        arg (int): Integer.\n"
                '    """\n'
                "    return\n"
            ),
            0,
        )

    def test_working_one_arg_no_return_type(self):
        self.write_str_and_assert_exception(
            (
                "def one_arg_no_return_type(arg: int):\n"
                '    """\n'
                "    One argument with no -> return type.\n"
                "\n"
                "    Args:\n"
                "    arg (int): Integer.\n"
                '    """\n'
                "    return\n"
            ),
            0,
        )

    def test_working_multiple_args(self):
        self.write_str_and_assert_exception(
            (
                "def multiple_args(arg1: int, arg2: float, arg3: str) -> None:\n"
                '    """\n'
                "    Multiple arguments.\n"
                "\n"
                "    Args:\n"
                "        arg1 (int): Integer.\n"
                "        arg2 (float): Float.\n"
                "        arg3 (str): str.\n"
                '    """\n'
                "    return\n"
            ),
            0,
        )

    def test_working_multiple_args_and_kwargs(self):
        self.write_str_and_assert_exception(
            (
                "def multiple_args_and_kwargs(arg1: int, arg2: float, **kwargs) -> None:\n"
                '    """\n'
                "    Multiple arguments and keyword arguments.\n"
                "\n"
                "    Args:\n"
                "        arg1 (int): Integer.\n"
                "        arg2 (float): Float.\n"
                '    """\n'
                "    return\n"
            ),
            0,
        )


if __name__ == "__main__":
    unittest.main()
