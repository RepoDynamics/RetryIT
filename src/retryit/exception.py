from typing import Any, Callable


class ReturnValueError(Exception):
    """
    Exception class for return value errors.
    """

    def __init__(
        self,
        return_value: Any,
        response_verifier: Callable[[Any], bool]
    ):
        self.return_value = return_value
        self.response_verifier = response_verifier
        error_msg = (
            f"Response verifier function {response_verifier} failed to verify {response_value}."
        )
        super().__init__(error_msg)
        return
