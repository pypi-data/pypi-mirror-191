from huble.error.exceptions import FunctionRuntimeException


def function_error_handling(name: str):

    """
    Decorator for handling errors while calling functions in Huble.
    """

    def wrapper(func):
        def wrapped(**kwargs):

            try:
                func(**kwargs)
            except Exception as e:
                raise FunctionRuntimeException(
                    f"{name} failed to execute. Error: {e}. Parameters given: {kwargs}"
                )

        return wrapped

    return wrapper
