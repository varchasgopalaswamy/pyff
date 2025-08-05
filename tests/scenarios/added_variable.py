MODULE_LEVEL_VARIABLE = 123


def top_level_function(arg1, arg2="default"):
    """This is a top-level function."""
    local_var = arg1
    print(f"Hello, {local_var} and {arg2}!")


class MyClass:
    """A class with methods."""

    def __init__(self, value):
        self.value = value

    def method_one(self):
        """A method."""
        print(f"Method one called with {self.value}")
