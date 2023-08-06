from dataclasses import dataclass
from typing import Generic, NoReturn, TypeVar


E = TypeVar("E", covariant=True)


def raise_exception(x: BaseException) -> NoReturn:
    raise x


@dataclass(frozen=True)
class RaiseLeft(Generic[E], Exception):
    value: E
