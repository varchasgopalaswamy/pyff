from pyff.kitchensink import hlistify, hl, pluralize


def test_hl():
    """Test hl() function."""
    assert hl("foo") == "``foo''"


def test_pluralize():
    """Test pluralize() function."""
    assert pluralize("item", []) == "items"
    assert pluralize("item", [1]) == "item"
    assert pluralize("item", [1, 2]) == "items"


def test_hlistify():
    """Test hlistify() function."""
    assert hlistify([]) == ""
    assert hlistify(["foo"]) == "``foo''"
    assert hlistify(["foo", "bar"]) == "``foo'', ``bar''"
