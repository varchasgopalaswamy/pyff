import os
from sys import version_info

CONSTANT = "value"

def top_level_function(arg1, arg2="default"):
    """This is a function."""
    if version_info > (3, 0):
        print("Python 3")
    else:
        print("Python 2")
    return os.path.join(str(arg1), str(arg2))

class MyClass:
    """A class with methods."""
    def __init__(self, value):
        self.value = value

    def method_one(self):
        """A simple method."""
        # A change in the method
        return self.value * 2

    def _private_method(self):
        """A private method."""
        return self.value + 1
