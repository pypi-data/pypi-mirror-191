class CodeGenerationException(Exception):
    """Exception raised when code generation fails."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class FunctionRuntimeException(Exception):
    """Exception raised when a function fails."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ParamsException(Exception):
    """Exception raised when params are mismatch."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
