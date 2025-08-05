"""A file with a changed function body."""

def foo():
    """A simple function."""
    a = 1
    b = 2
    return a - b  # Changed from + to -

class Bar:
    """A simple class."""
    def __init__(self):
        self.x = 1

    def baz(self):
        """A simple method."""
        return self.x + 1
