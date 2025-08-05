def my_decorator(func):
    """A simple decorator, but changed."""

    def wrapper(*args, **kwargs):
        print("Something different is happening before the function is called.")
        func(*args, **kwargs)
        print("Something different is happening after the function is called.")

    return wrapper


@my_decorator
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
