import os
from sys import version_info

CONSTANT = "value"

class MyClass:
    """A class with methods."""
    def __init__(self, value):
        self.value = value

    def method_one(self):
        """A simple method."""
        return self.value

    def _private_method(self):
        """A private method."""
        return self.value + 1
