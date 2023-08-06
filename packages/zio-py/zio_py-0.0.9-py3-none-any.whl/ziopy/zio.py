import functools
from dataclasses import dataclass
from typing import Callable, Generic, NoReturn, Tuple, Type, TypeVar, Union

from typing_extensions import Concatenate, ParamSpec

from ziopy.either import Either, Left, Right
from ziopy.util import RaiseLeft, raise_exception

"""
Heavily inspired by:
https://github.com/jdegoes/functional-effects/blob/master/src/main/scala/net/degoes/zio/00-intro.scala
"""


R = TypeVar('R', contravariant=True)
E = TypeVar('E', covariant=True)
A = TypeVar('A', covariant=True)
B = TypeVar('B')

G = TypeVar('G', bound=BaseException, covariant=True)

RR = TypeVar('RR')
EE = TypeVar('EE')
AA = TypeVar('AA')
BB = TypeVar('BB')

E2 = TypeVar('E2')
A2 = TypeVar('A2')

T = TypeVar('T')
Thunk = Callable[[], T]

P = ParamSpec("P")
F = TypeVar('F', bound=Callable)

X = TypeVar('X', bound=BaseException)


@dataclass(frozen=True)
class TypeMatchException(Generic[AA], Exception):
    value: AA


class ZIO(Generic[R, E, A]):
    def __init__(self, run: Callable[[R], Either[E, A]]):
        self._run = run

    @staticmethod
    def succeed(a: AA) -> "ZIO[object, NoReturn, AA]":
        return ZIO(lambda _: Right(a))

    @staticmethod
    def fail(e: EE) -> "ZIO[object, EE, NoReturn]":
        return ZIO(lambda _: Left(e))

    @staticmethod
    def from_either(e: Either[EE, AA]) -> "ZIO[object, EE, AA]":
        return ZIO(lambda _: e)

    @staticmethod
    def effect(side_effect: Thunk[AA]) -> "ZIO[object, Exception, AA]":
        a = ZIO[object, NoReturn, AA](lambda _: Either.right(side_effect()))
        return a.catch(Exception)

    @staticmethod
    def effect_catch(side_effect: Thunk[AA], exception_type: Type[X]) -> "ZIO[object, X, AA]":
        a = ZIO[object, NoReturn, AA](lambda _: Either.right(side_effect()))
        return a.catch(exception_type)

    @staticmethod
    def access(f: Callable[[R], AA]) -> "ZIO[R, NoReturn, AA]":
        return ZIO(lambda r: Right(f(r)))

    @staticmethod
    def access_m(f: Callable[[RR], "ZIO[RR, EE, AA]"]) -> "ZIO[RR, EE, AA]":
        return ZIO(lambda r: f(r)._run(r))

    def provide(self, r: R) -> "ZIO[object, E, A]":
        return ZIO(lambda _: self._run(r))

    @staticmethod
    def effect_total(side_effect: Thunk[AA]) -> "ZIO[object, NoReturn, AA]":
        return ZIO(lambda _: Right(side_effect()))

    def catch(
        self: "ZIO[R, E, AA]",
        exc: Type[X]
    ) -> "ZIO[R, Union[E, X], AA]":
        def _f(r: R) -> Either[Union[E, X], AA]:
            try:
                return self._run(r)
            except exc as e:
                return Either.left(e)
        return ZIO(_f)

    def map(self, f: Callable[[A], B]) -> "ZIO[R, E, B]":
        return ZIO(lambda r: self._run(r).map(f))

    def map_error(self: "ZIO[RR, EE, AA]", f: Callable[[EE], E2]) -> "ZIO[RR, E2, AA]":
        return ZIO(lambda r: self._run(r).map_left(f))

    def flat_map(
        self: "ZIO[RR, E, AA]",
        f: Callable[[AA], "ZIO[RR, EE, B]"]
    ) -> "ZIO[RR, Union[E, EE], B]":
        return ZIO(lambda r: self._run(r).flat_map(lambda a: f(a)._run(r)))

    def flatten(
        self: "ZIO[R, E, ZIO[R, EE, AA]]"
    ) -> "ZIO[R, Union[E, EE], AA]":
        return self.flat_map(lambda x: x)

    def __lshift__(self: "ZIO[RR, EE, AA]", other: "ZIO[RR, EE, B]") -> "ZIO[RR, EE, B]":
        return self.flat_map(lambda _: other)

    def zip(
        self: "ZIO[RR, E, AA]",
        that: "ZIO[RR, EE, B]"
    ) -> "ZIO[RR, Union[E, EE], Tuple[AA, B]]":
        return self.flat_map(lambda a: that.map(lambda b: (a, b)))

    def either(self) -> "ZIO[R, NoReturn, Either[E, A]]":
        return ZIO(lambda r: Right(self._run(r)))

    def absolve(self: "ZIO[R, E, Either[EE, AA]]") -> "ZIO[R, Union[E, EE], AA]":
        return self.flat_map(ZIO.from_either)

    def or_die(self: "ZIO[R, X, AA]") -> "ZIO[R, NoReturn, AA]":
        return ZIO(lambda r: self._run(r).fold(raise_exception, lambda a: Right(a)))

    def require(
        self: "ZIO[R, E, AA]",
        predicate: Callable[[AA], bool],
        to_error: Callable[[AA], EE]
    ) -> "ZIO[R, Union[E, EE], AA]":
        return ZIO(lambda r: self._run(r).require(predicate, to_error))

    def asserting(
        self: "ZIO[R, E, AA]",
        predicate: Callable[[AA], bool],
        to_error: Callable[[AA], X]
    ) -> "ZIO[R, E, AA]":
        return ZIO(lambda r: self._run(r).asserting(predicate, to_error))

    def or_else(
        self: "ZIO[R, EE, AA]",
        other: "ZIO[R, E2, A2]"
    ) -> "ZIO[R, Union[EE, E2], Union[AA, A2]]":
        return ZIO(
            lambda r: self._run(r).fold(
                lambda e: other._run(r),
                lambda a: Right(a)
            )
        )

    def swap(self: "ZIO[R, EE, AA]") -> "ZIO[R, AA, EE]":
        return ZIO(lambda r: self._run(r).swap())

    def match_types(self: "ZIO[R, E, AA]") -> "ZIO[R, E, NoReturn]":
        def _f(arg: AA) -> NoReturn:
            raise TypeMatchException(arg)
        return self.map(_f)

    def at_type(
        self: "ZIO[RR, EE, AA]",
        target_type: Type[A2],
        operation: "ZIO[A2, E2, BB]"
    ) -> "ZIO[RR, Union[EE, E2], Union[AA, BB]]":
        def _recover(arg: Union[EE, TypeMatchException]) -> ZIO[object, Union[EE, E2], BB]:
            if not isinstance(arg, TypeMatchException):
                return ZIO.fail(arg)
            if isinstance(arg.value, target_type):
                return operation.provide(arg.value)
            else:
                raise arg from arg

        return (
            self
            .catch(TypeMatchException)
            .swap()
            .either()
            .flat_map(lambda e: e.fold(ZIO.succeed, _recover))
        )


class Environment(Generic[R], ZIO[R, NoReturn, R]):
    def __init__(self) -> None:
        self._run = lambda r: Right(r)


def unsafe_run(io: ZIO[object, X, AA]) -> AA:
    return io._run(None).fold(raise_exception, lambda a: a)


class ZIOMonad(Generic[R, EE]):
    def __init__(self, environment: R) -> None:
        self._environment = environment

    def __lshift__(self, arg: ZIO[R, EE, BB]) -> BB:
        return arg._run(self._environment).fold(
            lambda e: raise_exception(RaiseLeft(e)),
            lambda a: a
        )


def monadic_method(
    func: Callable[Concatenate[AA, ZIOMonad[R, E], P], ZIO[R, E, A]]
) -> Callable[Concatenate[AA, P], ZIO[R, E, A]]:
    @functools.wraps(func)
    def _wrapper(self_arg: AA, *args: P.args, **kwargs: P.kwargs) -> ZIO[R, E, A]:
        def _catch_left(environment: R) -> ZIO[R, E, A]:
            try:
                return func(self_arg, ZIOMonad(environment), *args, **kwargs)
            except RaiseLeft as raise_left:
                # NOTE: WJH (12/20/20) mypy can't prove that the generic type
                #       of the _RaiseLeft instance here is `E`, so we have to
                #       use `type: ignore`.
                return ZIO.fail(raise_left.value)  # type: ignore

        return Environment[R]().flat_map(_catch_left)
    return _wrapper


def monadic(
    func: Callable[Concatenate[ZIOMonad[R, E], P], ZIO[R, E, A]]
) -> Callable[P, ZIO[R, E, A]]:
    @functools.wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> ZIO[R, E, A]:
        def _catch_left(environment: R) -> ZIO[R, E, A]:
            try:
                return func(ZIOMonad(environment), *args, **kwargs)
            except RaiseLeft as raise_left:
                # NOTE: WJH (12/20/20) mypy can't prove that the generic type
                #       of the _RaiseLeft instance here is `E`, so we have to
                #       use `type: ignore`.
                return ZIO.fail(raise_left.value)  # type: ignore

        return Environment[R]().flat_map(_catch_left)
    return _wrapper


class ZIOArrow(Generic[P, R, E, A]):
    @staticmethod
    def from_zio(zio: ZIO[R, E, Callable[P, A]]) -> "ZIOArrow[P, R, E, A]":
        return ZIOArrow(lambda *args, **kwargs: zio.map(lambda f: f(*args, **kwargs)))

    @staticmethod
    def from_callable(f: Callable[P, A]) -> "ZIOArrow[P, object, NoReturn, A]":
        return ZIOArrow(lambda *args, **kwargs: ZIO.succeed(f(*args, **kwargs)))

    def __init__(self, f: Callable[P, ZIO[R, E, A]]) -> None:
        self._f = f

    def to_callable(self) -> "Callable[P, ZIO[R, E, A]]":
        return self._f

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> "ZIO[R, E, A]":
        return self._f(*args, **kwargs)

    def provide(self, r: R) -> "ZIOArrow[P, object, E, A]":
        return ZIOArrow(lambda *args, **kwargs: self._f(*args, **kwargs).provide(r))

    def catch(
        self: "ZIOArrow[P, R, E, AA]",
        exc: Type[X]
    ) -> "ZIOArrow[P, R, Union[E, X], AA]":
        def _g(*args: P.args, **kwargs: P.kwargs) -> ZIO[R, Union[E, X], AA]:
            try:
                return self._f(*args, **kwargs)
            except exc as e:
                return ZIO.fail(e)
        return ZIOArrow(_g)

    def map(self, f: Callable[[A], B]) -> "ZIOArrow[P, R, E, B]":
        return ZIOArrow(lambda *args, **kwargs: self._f(*args, **kwargs).map(f))

    def map_error(
        self: "ZIOArrow[P, RR, EE, AA]", f: Callable[[EE], E2]
    ) -> "ZIOArrow[P, RR, E2, AA]":
        return ZIOArrow(lambda *args, **kwargs: self._f(*args, **kwargs).map_error(f))

    def flat_map(
        self: "ZIOArrow[P, RR, E, AA]",
        f: Callable[[AA], "ZIO[RR, EE, B]"]
    ) -> "ZIOArrow[P, RR, Union[E, EE], B]":
        return ZIOArrow(lambda *args, **kwargs: self._f(*args, **kwargs).flat_map(f))

    def flatten(
        self: "ZIOArrow[P, R, E, ZIO[R, EE, AA]]"
    ) -> "ZIOArrow[P, R, Union[E, EE], AA]":
        return self.flat_map(lambda x: x)

    def __lshift__(
        self: "ZIOArrow[P, RR, EE, AA]", other: "ZIO[RR, EE, B]"
    ) -> "ZIOArrow[P, RR, EE, B]":
        return self.flat_map(lambda _: other)

    def zip(
        self: "ZIOArrow[P, RR, E, AA]",
        that: "ZIO[RR, EE, B]"
    ) -> "ZIOArrow[P, RR, Union[E, EE], Tuple[AA, B]]":
        return self.flat_map(lambda a: that.map(lambda b: (a, b)))

    def either(self) -> "ZIOArrow[P, R, NoReturn, Either[E, A]]":
        return ZIOArrow(lambda *args, **kwargs: self._f(*args, **kwargs).either())

    def absolve(
        self: "ZIOArrow[P, R, E, Either[EE, AA]]"
    ) -> "ZIOArrow[P, R, Union[E, EE], AA]":
        return self.flat_map(ZIO.from_either)

    def or_die(self: "ZIOArrow[P, R, X, AA]") -> "ZIOArrow[P, R, NoReturn, AA]":
        return ZIOArrow(lambda *args, **kwargs: self._f(*args, **kwargs).or_die())

    def require(
        self: "ZIOArrow[P, R, E, AA]",
        predicate: Callable[[AA], bool],
        to_error: Callable[[AA], EE]
    ) -> "ZIOArrow[P, R, Union[E, EE], AA]":
        return ZIOArrow(
            lambda *args, **kwargs: self._f(*args, **kwargs).require(predicate, to_error)
        )

    def asserting(
        self: "ZIOArrow[P, R, E, AA]",
        predicate: Callable[[AA], bool],
        to_error: Callable[[AA], X]
    ) -> "ZIOArrow[P, R, E, AA]":
        return ZIOArrow(
            lambda *args, **kwargs: self._f(*args, **kwargs).asserting(predicate, to_error)
        )

    def or_else(
        self: "ZIOArrow[P, R, EE, AA]",
        other: "ZIO[R, E2, A2]"
    ) -> "ZIOArrow[P, R, Union[EE, E2], Union[AA, A2]]":
        return ZIOArrow(lambda *args, **kwargs: self._f(*args, **kwargs).or_else(other))

    def swap(self: "ZIOArrow[P, R, EE, AA]") -> "ZIOArrow[P, R, AA, EE]":
        return ZIOArrow(lambda *args, **kwargs: self._f(*args, **kwargs).swap())

    def match_types(self: "ZIOArrow[P, R, E, AA]") -> "ZIOArrow[P, R, E, NoReturn]":
        return ZIOArrow(lambda *args, **kwargs: self._f(*args, **kwargs).match_types())

    def at_type(
        self: "ZIOArrow[P, RR, EE, AA]",
        target_type: Type[A2],
        operation: "ZIO[A2, E2, BB]"
    ) -> "ZIOArrow[P, RR, Union[EE, E2], Union[AA, BB]]":
        return ZIOArrow(
            lambda *args, **kwargs: self._f(*args, **kwargs).at_type(target_type, operation)
        )
