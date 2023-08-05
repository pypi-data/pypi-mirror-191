import dataclasses
from collections.abc import Callable, Coroutine
from typing import Any, Generic, TypeAlias, TypeVar
from pydantic import BaseModel


_T = TypeVar("_T")

ValidatorFunc: TypeAlias = Callable[[Any], Coroutine[Any, Any, None]]


class ErrorSchema(BaseModel, Generic[_T]):
    code: str
    message: str
    detail: str|None = None
    source: _T|None = None


class ValidationError(Generic[_T], Exception):
    messages: list[ErrorSchema[_T]]

    def __init__(
        self,
        messages: list[ErrorSchema[_T]],
        *args: object
    ) -> None:
        super().__init__(*args)
        self.messages = messages


@dataclasses.dataclass
class ValidationContext(Generic[_T]):
    _errors: list[ErrorSchema[_T]]

    def add_error(self, error: ErrorSchema[_T]) -> None:
        self._errors.append(error)

    def extend_nested_error(self, errors: list[ErrorSchema[_T]]) -> None:
        self._errors.extend(errors)

    @property
    def errors(self) -> list[ErrorSchema[_T]]:
        return self._errors
