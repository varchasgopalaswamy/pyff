"""Placeholders for various elements in output"""

from __future__ import annotations

import ast
from collections.abc import Iterable, Sized

from colorama import Fore, Style

HL_OPEN = "``"
HL_CLOSE = "''"

HIGHLIGHTS = ("color", "quotes")


def compare_ast(node1, node2):
    if type(node1) is not type(node2):
        return False
    if isinstance(node1, ast.AST):
        for k, v in vars(node1).items():
            if k in ("lineno", "col_offset", "ctx", "end_lineno", "end_col_offset"):
                continue
            if not compare_ast(v, getattr(node2, k)):
                return False
        return True
    if isinstance(node1, list):
        if len(node1) != len(node2):
            return False
        return all(compare_ast(n1, n2) for n1, n2 in zip(node1, node2))
    return node1 == node2


def highlight(message: str, highlights: str) -> str:
    """Replace highlight placeholders in a given string using selected method"""
    if highlights == "color":
        return message.replace(HL_OPEN, Fore.RED).replace(HL_CLOSE, Style.RESET_ALL)
    if highlights == "quotes":
        return message.replace(HL_OPEN, "'").replace(HL_CLOSE, "'")

    raise ValueError("Highlight should be one of: " + str(HIGHLIGHTS))


def hl(what: str) -> str:  # pylint: disable=invalid-name
    """Return highlighted string"""
    return f"{HL_OPEN}{what}{HL_CLOSE}"


def pluralize(name: str, items: Sized) -> str:
    """Return a pluralized name unless there is exactly one element in container."""
    return f"{name}" if len(items) == 1 else f"{name}s"


def hlistify(container: Iterable) -> str:
    """Returns a comma separated list of highlighted names."""
    return ", ".join([hl(name) for name in container])
