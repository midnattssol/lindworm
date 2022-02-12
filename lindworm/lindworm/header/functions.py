"""Header functions for Lindworm."""
import typing as t
import itertools as it


_IOTA = 0


def iota(zero=False) -> int:
    global _IOTA
    if zero:
        _IOTA = 0
    else:
        _IOTA += 1
    return _IOTA


def curry(fn: t.Callable, *args, **kwargs) -> t.Callable:
    return lambda *args_, **kwargs_: fn(*args, *args_, **kwargs, **kwargs)


def compose(left, right, reverse, num_stars) -> t.Callable:
    """Returns left `of` right, or right `of` left if reversed."""
    if reverse:
        left, right = right, left

    if num_stars == 1:
        return lambda *args, **kwargs: left(*right(*args, **kwargs))
    if num_stars == 2:
        return lambda *args, **kwargs: left(**right(*args, **kwargs))

    return lambda *args, **kwargs: left(right(*args, **kwargs))
