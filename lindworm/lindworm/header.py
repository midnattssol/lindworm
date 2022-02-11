"""Header functions for Lindworm."""
import functools as ft
import itertools as it
import more_itertools as mit
import dataclasses as dc
import typing as t
import numpy


@dc.dataclass
class LindwormIteratorSlicer:
    """A class for slicing iterators."""
    iterator: t.Iterator

    def __getitem__(self, index):
        if isinstance(index, int):
            for _ in range(index):
                next(self.iterator)
            return next(self.iterator)
        if isinstance(index, slice):
            return mit.islice_extended(self.iterator, index.start, index.stop, index.step)

        raise TypeError(f"{type(self).__qualname__} indices must be integers or slices, not {type(index).__qualname__}")


def curry(fn: t.Callable, *args, **kwargs) -> t.Callable:
    return lambda *args_, **kwargs_: fn(*args, *args_, **kwargs, **kwargs)


def compose(left, right, left_to_right, *, stars=0) -> t.Callable:
    if left_to_right:
        left, right = right, left

    if stars == 1:
        return lambda *args, **kwargs: left(*right(*args, **kwargs))
    if stars == 2:
        return lambda *args, **kwargs: left(**right(*args, **kwargs))

    return lambda *args, **kwargs: left(right(*args, **kwargs))


_IOTA = 0


def iota() -> int:
    global _IOTA
    _IOTA += 1
    return _IOTA


def zero_iota() -> int:
    global _IOTA
    _IOTA = 0
    return _IOTA
