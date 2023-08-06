import ast

from python_code_parse.exceptions import FunctionNotFoundException
from python_code_parse.models.function_info import FunctionInfo


def get_function_indentation_str(code: str, function_name: str) -> str:
    """Get the indentation string of a function in a given code string."""

    tree: ast.Module = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name != function_name:
                continue

            return " " * node.col_offset

    raise FunctionNotFoundException(
        f"Function {function_name} not found in code"
    )
