"""This module contains code that handles comparing modules"""

from __future__ import annotations

import ast
import logging
import pathlib

import pyff.classes as pc
import pyff.functions as pf
import pyff.imports as pi
from pyff.kitchensink import hl, hlistify, pluralize

LOGGER = logging.getLogger(__name__)


class ModuleSummary:  # pylint: disable=too-few-public-methods
    """Holds summary information about a module"""

    def __init__(self, name: str, node: ast.Module) -> None:
        self.name: str = name
        self.node: ast.Module = node


class ModulePyfference:  # pylint: disable=too-few-public-methods
    """Holds differences between two Python modules"""

    def __init__(
        self,
        imports: pi.ImportsPyfference | None = None,
        classes: pc.ClassesPyfference | None = None,
        functions: pf.FunctionsPyfference | None = None,
    ) -> None:
        self.other: list = []
        self.imports: pi.ImportsPyfference | None = imports
        self.classes: pc.ClassesPyfference | None = classes
        self.functions: pf.FunctionsPyfference | None = functions

    def __str__(self):
        changes = [self.imports, self.classes, self.functions] + self.other
        return "\n".join([str(change) for change in changes if change is not None])

    def simplify(self) -> ModulePyfference | None:
        """Cleans empty differences, empty sets etc. after manipulation"""
        if self.imports is not None:
            self.imports = self.imports.simplify()

        if self.classes is not None:
            self.classes = self.classes.simplify()

        if self.functions is not None:
            self.functions = self.functions.simplify()

        return (
            self
            if (self.functions or self.classes or self.imports or self.other)
            else None
        )


class ModulesPyfference:  # pylint: disable=too-few-public-methods
    """Holds difference between modules in a package"""

    def __init__(
        self,
        removed: dict[pathlib.Path, ModuleSummary],
        changed: dict[pathlib.Path, ModulePyfference],
        new: dict[pathlib.Path, ModuleSummary],
    ) -> None:
        self.removed: dict[pathlib.Path, ModuleSummary] = removed
        self.changed: dict[pathlib.Path, ModulePyfference] = changed
        self.new: dict[pathlib.Path, ModuleSummary] = new

    def __str__(self):
        lines = []

        if self.removed:
            lines.append(
                f"Removed {pluralize('module', self.removed)} {hlistify(sorted(self.removed))}"
            )

        if self.changed:
            lines.append(
                "\n".join(
                    [
                        f"Module {hl(module)} changed:\n  "
                        + str(change).replace("\n", "\n  ")
                        for module, change in sorted(self.changed.items())
                    ]
                )
            )

        if self.new:
            lines.append(
                f"New {pluralize('module', self.new)} {hlistify(sorted(self.new))}"
            )

        return "\n".join(lines)

    def __repr__(self):
        return (
            f"ModulesPyfference(removed={self.removed!r}, "
            f"changed={self.changed!r}, new={self.new!r})"
        )

    def __bool__(self):
        return bool(self.removed or self.changed or self.new)


def summarize_module(module: pathlib.Path) -> ModuleSummary:
    """Return a ModuleSummary of a given module"""
    return ModuleSummary(name=module.name, node=ast.parse(module.read_text()))


def pyff_module(old: ModuleSummary, new: ModuleSummary) -> ModulePyfference | None:
    """Return difference between two Python modules, or None if they are identical"""
    old_imports = pi.ImportedNames.extract(old.node)
    new_imports = pi.ImportedNames.extract(new.node)
    imports = pi.pyff_imports(old.node, new.node)
    classes = pc.pyff_classes(old.node, new.node, old_imports, new_imports)
    functions = pf.pyff_functions(old.node, new.node, old_imports, new_imports)

    if imports or classes or functions:
        LOGGER.debug("Modules differ")
        return ModulePyfference(imports, classes, functions)

    LOGGER.debug("Modules are identical")
    return None


def pyff_module_path(old: pathlib.Path, new: pathlib.Path) -> ModulePyfference | None:
    """Return difference between two Python modules, or None if they are identical"""
    return pyff_module(summarize_module(old), summarize_module(new))
