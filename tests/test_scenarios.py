import pathlib

from pyff.modules import pyff_module_path

SCENARIOS_DIR = pathlib.Path(__file__).parent / "scenarios"
BASE_MODULE = SCENARIOS_DIR / "base.py"


def test_no_change():
    """Tests that pyff reports no changes for identical files."""
    diff = pyff_module_path(BASE_MODULE, BASE_MODULE)
    assert diff is None


def test_added_function():
    """Tests that pyff detects a new function."""
    changed_module = SCENARIOS_DIR / "added_function.py"
    diff = pyff_module_path(BASE_MODULE, changed_module)
    assert diff is not None
    assert diff.functions is not None
    assert "new_function" in diff.functions.new
    assert len(diff.functions.new) == 1
    assert not diff.functions.removed
    assert not diff.functions.changed
    assert diff.classes is None
    assert diff.imports is None


def test_removed_function():
    """Tests that pyff detects a removed function."""
    changed_module = SCENARIOS_DIR / "removed_function.py"
    diff = pyff_module_path(BASE_MODULE, changed_module)
    assert diff is not None
    assert diff.functions is not None
    assert "top_level_function" in diff.functions.removed
    assert len(diff.functions.removed) == 1
    assert not diff.functions.new
    assert not diff.functions.changed
    assert diff.classes is None
    assert diff.imports is None


def test_changed_function_body():
    """Tests that pyff detects a change in function body."""
    changed_module = SCENARIOS_DIR / "changed_function_body.py"
    diff = pyff_module_path(BASE_MODULE, changed_module)
    assert diff is not None
    assert diff.functions is not None
    assert "top_level_function" in diff.functions.changed
    assert len(diff.functions.changed) == 1
    assert not diff.functions.new
    assert not diff.functions.removed
    assert diff.classes is None
    assert diff.imports is None
    change = diff.functions.changed["top_level_function"]
    assert change.implementation
    assert len(change.implementation) > 0


def test_added_class():
    """Tests that pyff detects a new class."""
    changed_module = SCENARIOS_DIR / "added_class.py"
    diff = pyff_module_path(BASE_MODULE, changed_module)
    assert diff is not None
    assert diff.classes is not None
    assert any(c.name == "NewClass" for c in diff.classes.new)
    assert len(diff.classes.new) == 1
    assert not diff.classes.changed
    assert diff.functions is None
    assert diff.imports is None


def test_added_decorator():
    """Tests that pyff detects a new decorator on a function."""
    changed_module = SCENARIOS_DIR / "added_decorator.py"
    diff = pyff_module_path(BASE_MODULE, changed_module)
    assert diff is not None
    assert diff.functions is not None
    assert "my_decorator" in diff.functions.new
    assert len(diff.functions.new) == 1
    assert "top_level_function" in diff.functions.changed
    assert len(diff.functions.changed) == 1
    assert not diff.functions.removed
    assert diff.classes is None
    assert diff.imports is None
    change = diff.functions.changed["top_level_function"]
    assert change.implementation
    assert len(change.implementation) > 0


def test_removed_decorator():
    """Tests that pyff detects a removed decorator from a function."""
    old_module = SCENARIOS_DIR / "added_decorator.py"
    diff = pyff_module_path(old_module, BASE_MODULE)
    assert diff is not None
    assert diff.functions is not None
    assert "my_decorator" in diff.functions.removed
    assert len(diff.functions.removed) == 1
    assert "top_level_function" in diff.functions.changed
    assert len(diff.functions.changed) == 1
    assert not diff.functions.new
    assert diff.classes is None
    assert diff.imports is None
    change = diff.functions.changed["top_level_function"]
    assert change.implementation
    assert len(change.implementation) > 0


def test_changed_decorator():
    """Tests that pyff detects a change in a decorator function."""
    old_module = SCENARIOS_DIR / "added_decorator.py"
    new_module = SCENARIOS_DIR / "changed_decorator.py"
    diff = pyff_module_path(old_module, new_module)
    assert diff is not None
    assert diff.functions is not None
    assert "my_decorator" in diff.functions.changed
    assert len(diff.functions.changed) == 1
    assert not diff.functions.new
    assert not diff.functions.removed
    assert "top_level_function" not in diff.functions.changed
    assert diff.classes is None
    assert diff.imports is None


def test_added_variable():
    """Tests that pyff detects a new module-level variable."""
    changed_module = SCENARIOS_DIR / "added_variable.py"
    diff = pyff_module_path(BASE_MODULE, changed_module)
    assert diff is not None, "pyff does not seem to detect module-level variables"
    assert diff.functions is None
    assert diff.classes is None
    assert diff.imports is None


def test_changed_class_method():
    """Tests that pyff detects a change in a class method."""
    changed_module = SCENARIOS_DIR / "changed_class_method.py"
    diff = pyff_module_path(BASE_MODULE, changed_module)
    assert diff is not None
    assert diff.classes is not None
    assert "MyClass" in diff.classes.changed
    assert len(diff.classes.changed) == 1
    assert not diff.classes.new

    class_change = diff.classes.changed["MyClass"]
    assert class_change.methods is not None
    assert "method_one" in class_change.methods.changed
    assert len(class_change.methods.changed) == 1
    assert not class_change.methods.new
    assert not class_change.methods.removed

    assert diff.functions is None
    assert diff.imports is None
