#!/usr/bin/env python3.10
from .result import Err, Ok, Result, UnwrapError

"""New builtins for Lindworm."""

from functools import reduce as fold_right
from itertools import (chain, combinations, count, groupby, permutations,
                       product)

from more_itertools import (adjacent, always_iterable, always_reversible,
                            bucket, circular_shifts, collapse,
                            combination_index, consume, consumer, convolve,
                            countable, distinct_combinations,
                            distinct_permutations, duplicates_everseen,
                            duplicates_justseen, first_true, flatten, ilen,
                            is_sorted, iter_except, iterate, locate, lstrip,
                            minmax, nth_combination, nth_or_last,
                            nth_permutation, nth_product, numeric_range,
                            partitions, permutation_index, powerset,
                            product_index, repeat_last, replace, rlocate,
                            rstrip, set_partitions, sliding_window,
                            split_after, split_at, split_before, split_into,
                            split_when, spy, strip, unique_everseen,
                            unique_in_window, unique_justseen, unique_to_each,
                            with_iter)


def fold_left(*args):
    """Left fold."""
    return fold_right(args[0], reversed(args[1]), *args[2:])
