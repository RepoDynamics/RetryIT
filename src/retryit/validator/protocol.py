from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Validator(Protocol):
    def stop(self, value: Any, exception: Exception | None) -> bool:
        ...

    @property
    def sleep_seconds(self) -> int | float:
        ...

    @property
    def exception(self) -> Exception | None:
        ...

    @property
    def value(self) -> Any:
        ...
