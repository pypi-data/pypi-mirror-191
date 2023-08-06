import functools
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, Generic
from business_validator.types import (
    ErrorSchema,
    ValidationContext,
    ValidationError,
    ValidatorFunc,
    _T,
)


def validate(name: str | None = None) -> Callable[[ValidatorFunc], ValidatorFunc]:
    def decorator(f: ValidatorFunc) -> ValidatorFunc:
        @wraps(f)
        async def wrapper(self: Validator[Any]) -> None:
            await f(self)

        wrapper.name = name  # type: ignore[attr-defined]
        wrapper.__is_validator__ = True  # type: ignore[attr-defined]

        return wrapper

    return decorator


class Validator(Generic[_T]):
    async def validate(self) -> None:
        context = self.context

        for validator in self.get_validation_methods():
            await validator(self)

        if context.errors:
            raise ValidationError(context.errors)

    @functools.cached_property
    def context(self) -> ValidationContext[_T]:
        return ValidationContext(_errors=[])

    async def errors(self) -> list[ErrorSchema[_T]]:
        try:
            await self.validate()
        except ValidationError as e:
            return e.messages
        return []

    @classmethod
    def get_validation_methods(
        cls,
    ) -> list[Callable[["Validator[_T]"], Awaitable[None]]]:
        return [
            value
            for value in cls.__dict__.values()
            if getattr(value, "__is_validator__", False)
        ]
