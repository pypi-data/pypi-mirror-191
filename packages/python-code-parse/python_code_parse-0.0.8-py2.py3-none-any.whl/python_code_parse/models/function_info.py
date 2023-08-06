from typing import List, NamedTuple

from python_code_parse.models.function_arg import FunctionArg


class FunctionInfo(NamedTuple):
    """A dataclass to hold information about a function."""

    name: str
    args: List[FunctionArg]
    return_type: str
    line: int
    signature_end_line_index: int
