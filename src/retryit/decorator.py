from typing import Callable
import time
from functools import wraps
from retryit.validator.protocol import Validator
from retryit.validator.default import DefaultValidator


def retry(
    function: Callable | None = None,
    *,
    validator: Validator = DefaultValidator(),
) -> Callable:
    """
    Decorator to retry a function call for a given number of times
    (while waiting for a certain amount of time between calls),
    when one of the given exceptions is raised.

    Parameters
    ----------
    function : callable
        The function to be decorated.
    config : RetryConfig, default: RetryConfig(3, 1, 3)
        Retry configuration.
    catch : Type[Exception] | tuple[Type[Exception]], default: Exception
        Exception type(s) that will be ignored during the retries.
        All other exceptions will be raised immediately.

    Returns
    -------
    callable
        Decorated function.
    """
    if not isinstance(validator, Validator):
        raise TypeError("validator does not implement the Validator protocol.")

    def retry_decorator(func: Callable):

        @wraps(func)
        def retry_wrapper(*args, **kwargs):
            while True:
                try:
                    return_value = func(*args, **kwargs)
                    exception = None
                except Exception as e:
                    return_value = None
                    exception = e
                stop = validator.stop(return_value, exception)
                if stop:
                    if validator.exception:
                        raise validator.exception
                    return validator.value
                time.sleep(validator.sleep_seconds)

        return retry_wrapper

    return retry_decorator if function is None else retry_decorator(function)
