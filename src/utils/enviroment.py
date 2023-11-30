class Environment:
    def __init__(self, parent=None):
        """
        Initialize an environment with an optional parent environment.

        Parameters:
        - parent: The parent environment (default is None for the global scope).
        """
        self.variables_and_methods = {}  # A dictionary to store variable and method definitions.
        self.parent = parent  # Reference to the parent environment.
        self.definitions_count = 0  # Counter to track the number of definitions in this environment.

    def define(self, name, definition):
        """
        Define a variable or method in the current environment.

        Parameters:
        - name: The name of the variable or method.
        - definition: The reference to the variable or method.
        """
        self.variables_and_methods[name] = definition
        self.definitions_count += 1

    def get(self, name):
        """
        Retrieve the reference to a variable or method from the current or parent environment.

        Parameters:
        - name: The name of the variable or method to retrieve.

        Returns:
        - The reference to the variable or method, or None if not found.
        """
        if name in self.variables_and_methods:
            return self.variables_and_methods[name]

        if self.parent:
            return self.parent.get(name)

        return None