from typing import Any, Callable, Type

from retryit import sleeper
from retryit.exception import RetryError


class DefaultValidator:

    def __init__(
        self,
        sleep_calculator: Callable[[int, float], float] = sleeper.constant_until_max_duration(10, 600),
        catch: Type[Exception] | tuple[Type[Exception]] | None = Exception,
        value_verifier: Callable[[Any], bool] | None = None,
    ):

        if not catch and not value_verifier:
            raise ValueError("Either catch or value_verifier must be provided.")

        self._sleeper = sleep_calculator
        self._exceptions_to_catch = catch
        self._value_verifier = value_verifier

        self._count_tries = 0
        self._current_total_sleep_seconds = 0
        self._next_sleep_seconds = 0
        self._value = None
        self._exception = None
        self._history = []
        return

    def stop(self, value: Any, exception: Exception | None) -> bool:
        self._count_tries += 1
        self._value = value
        self._exception = exception
        self._history.append((exception is not None, exception or value))
        if exception:
            if not self._exceptions_to_catch or not isinstance(exception, self._exceptions_to_catch):
                return True
            if self._process():
                return True
            return False
        if self._value_verifier:
            if self._value_verifier(value):
                return True
            if self._process():
                return True
            return False
        return True

    @property
    def sleep_seconds(self) -> float:
        return self._next_sleep_seconds

    @property
    def exception(self) -> Exception | None:
        return self._exception

    @property
    def value(self) -> Any:
        return self._value

    def _process(self):
        next_sleep_seconds = self._sleeper(self._count_tries, self._current_total_sleep_seconds)
        if next_sleep_seconds == 0:
            self._exception = RetryError(
                count_tries=self._count_tries,
                total_sleep_seconds=self._current_total_sleep_seconds,
                history=self._history
            )
            return True
        self._next_sleep_seconds = next_sleep_seconds
        self._current_total_sleep_seconds += next_sleep_seconds
        return False


