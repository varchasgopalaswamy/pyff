import os
from sys import version_info

CONSTANT = "value"

def top_level_function(arg1, arg2="default"):
    """This is a function."""
    # This is a change
    if version_info > (3, 6):
        print("Python 3.6+")
    else:
        print("Older Python")
    return os.path.join(str(arg1), str(arg2))

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
