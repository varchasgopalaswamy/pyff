import pathlib
from pyff.modules import pyff_module_path

TEST_DATA_DIR = pathlib.Path(__file__).parent / "test_data"

def test_changed_function_body():
    """
    Tests that pyff detects a change in a function body.
    """
    base_path = TEST_DATA_DIR / "base.py"
    changed_path = TEST_DATA_DIR / "changed_function_body.py"

    diff = pyff_module_path(base_path, changed_path)
    assert diff is not None
    assert diff.functions is not None
    assert "foo" in diff.functions.changed
    assert not diff.functions.new
    assert not diff.functions.removed
    assert diff.classes is None
    assert diff.imports is None
