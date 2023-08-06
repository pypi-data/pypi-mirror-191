import ast

from python_code_parse.exceptions import FunctionNotFoundException
from python_code_parse.models.function_info import FunctionInfo


def get_signature_end_index(function_def: ast.FunctionDef) -> int:
    return function_def.body[0].lineno - 2


def replace_function_signature(code: str, function_info: FunctionInfo) -> str:
    """Replace the signature of a function in a given code string."""

    tree: ast.Module = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name != function_info.name:
                continue

            function_line_number = node.lineno
            spaces = " " * node.col_offset
            new_signature = f"{spaces}def {function_info.name}("

            for arg in function_info.args:
                if arg.annotation != "" and arg.annotation is not None:
                    new_signature += f"{arg.name}: {arg.annotation}, "
                else:
                    new_signature += f"{arg.name}, "

            if len(function_info.args) > 0:
                new_signature = new_signature[:-2]

            new_signature += ") -> " + function_info.return_type + ":"

            lines = code.splitlines()

            signature_end_line = get_signature_end_index(node)

            for _ in range(
                function_line_number - 1,
                signature_end_line + 1,
            ):
                lines.pop(function_line_number - 1)

            lines.insert(function_line_number - 1, new_signature)
            return "\n".join(lines)

    raise FunctionNotFoundException(
        f"Function {function_info.name} not found in code"
    )
