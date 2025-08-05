"""Entry point for the `pyff` command"""

from __future__ import annotations

import pathlib
import sys

import click
import loguru


@click.command()
@click.argument("old", type=click.Path(exists=True, path_type=pathlib.Path))
@click.argument("new", type=click.Path(exists=True, path_type=pathlib.Path))
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    default=False,
    help="Enable recursive processing of directories",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    default=False,
    help="Enable debug logging",
)
def pyff(old: pathlib.Path, new: pathlib.Path, *, recursive: bool, debug: bool) -> None:
    """Entry point for the `pyff` command."""
    if debug:
        # Set loguru to debug level
        loguru.logger.remove()
        loguru.logger.add(sys.stdout, level="DEBUG")
        loguru.logger.debug("Debug logging enabled")

    if old.is_dir() and new.is_dir():
        if recursive:
            old_files = list(old.rglob("**/*.py"))
            new_files = list(new.rglob("**/*.py"))
        else:
            old_files = list(old.glob("*.py"))
            new_files = list(new.glob("*.py"))
    elif old.is_file() and new.is_file():
        old_files = [old]

        new_files = [new]
    else:
        click.echo("Both old and new must be either directories or files.")
        sys.exit(1)

    old_files_relative = [f.relative_to(old) for f in old_files]
    new_files_relative = [f.relative_to(new) for f in new_files]

    changed = False
    for file in old_files_relative:
        if file not in new_files_relative:
            loguru.logger.info(f"File '{file}' was removed in new version")
            changed = True
    for file in new_files_relative:
        if file not in old_files_relative:
            loguru.logger.info(f"File '{file}' was added in new version")
            changed = True
    common_files = set(old_files_relative).intersection(set(new_files_relative))
    for file in common_files:
        old_path = old / file
        new_path = new / file
        loguru.logger.debug(f"Comparing '{old_path}' with '{new_path}'")

    if changed:
        loguru.logger.info(f"Found changes between '{old}' and '{new}'")
        sys.exit(1)
    else:
        loguru.logger.info(f"No changes found between '{old}' and '{new}'")
        sys.exit(0)


if __name__ == "__main__":
    pyff()
