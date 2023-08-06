from dataclasses import dataclass


@dataclass
class FunctionArg:
    """A dataclass to hold information about a function argument."""

    name: str
    annotation: str = None
