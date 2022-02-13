#!/usr/bin/env python3.10
import typing as t

T, V, E, Q, W = map(t.TypeVar, "TVEQW")
OriginalSignature = t.Callable[Q, W]


class UnwrapError(BaseException):
    """An error raised by the Result type on failed unwrappings."""


class Result(t.Generic[T]):
    def __init__(self):
        raise NotImplementedError(f"Instances of type `{type(self)}` should not be initialized directly.")

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: {self.contents!r}>"

    def unwrap(self) -> T:
        """Attempt to unwrap the value. Raises UnwrapError on failure."""
        if not self:
            raise UnwrapError
        return self.contents

    def unwrap_err(self) -> T:
        """Attempt to unwrap the value, expecting an Err. Raises UnwrapError on failure."""
        if self:
            raise UnwrapError
        return self.contents

    def expect(self, error_msg: str) -> T:
        """Attempt to unwrap the value. Raises UnwrapError with the error message on failure."""
        if not self:
            raise UnwrapError(error_msg)
        return self.contents

    def expect_err(self, error_msg: str) -> T:
        """Attempt to unwrap the value, expecting an Err. Raises UnwrapError with the error message on failure."""
        if self:
            raise UnwrapError(error_msg)
        return self.contents

    def unwrap_or(self, value: T) -> T:
        """Attempt to unwrap the value. Returns `value` on failure."""
        return self.unwrap() if self else value

    def unwrap_or_else(self, func: t.Callable[[], T]) -> T:
        """Attempt to unwrap the value. Returns `func()` on failure."""
        return self.unwrap() if self else func()

    def is_ok(self) -> bool:
        """Returns a bool corresponding to whether or not the item is Ok."""
        return bool(self)

    def is_err(self) -> bool:
        """Returns a bool corresponding to whether or not the item is Err."""
        return not bool(self)

    def copy(self):
        """Returns a copy of the item."""
        return type(self)(self.contents)

    def __eq__(self, other):
        return (
            self.is_ok() == other.is_ok()
            and self.unwrap() == other.unwrap()
        )

    @classmethod
    def from_iterator(cls, iterator):
        """Turns an iterator of Result instances to a Result containing an iterator.

        If any of the items of the iterator is Err, the function short-circuits and returns this Err.
        Note that this might mean that the iterable is not guaranteed to be exhausted."""
        contents = []
        for item in iterator:
            if item.is_err():
                return item
            if not isinstance(item, Result):
                raise TypeError(f"Result.from_iterator only support Result instances, not {type(item)}")
            contents.append(item.unwrap())

        return Ok(contents)

    # === Decorators ===
    def wrap_with_closure(optional_func: t.Callable[[UnwrapError], t.Any] = (lambda x: ...)) -> t.Callable[OriginalSignature, OriginalSignature]:
        """
        Meta-decorator that calls `optional_func` on the exception and
        returns Err() if the function raises an UnwrapError.
        """
        def inner(func: OriginalSignature) -> OriginalSignature:
            def replacement_func(*args, **kwargs) -> Result[W]:
                try:
                    return Ok(func(*args, **kwargs))
                except UnwrapError as exception:
                    optional_func(exception)
                    return Err(exception)

            return replacement_func

        return inner

    def wrap(func: OriginalSignature) -> OriginalSignature:
        """Decorator that returns Err() if the function raises an UnwrapError."""
        return wrap_with_closure()(func)


class Ok(Result):
    def __init__(self, contents: V):
        self.contents = contents

    def __bool__(self):
        return True

    def __hash__(self):
        return hash((Ok, self.contents))

    def __iter__(self):
        return iter((self.contents,))


class Err(Result):
    def __init__(self, contents: E):
        self.contents = contents

    def __bool__(self):
        return False

    def __hash__(self):
        return hash((Err, self.contents))

    def __iter__(self):
        return iter(tuple())
