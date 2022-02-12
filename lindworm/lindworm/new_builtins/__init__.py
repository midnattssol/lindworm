#!/usr/bin/env python3.10
"""New builtins for Lindworm."""

from itertools import (
    chain,
    groupby,
    product,
    permutations,
    combinations,
    count
)

from more_itertools import (
    split_at,
    split_before,
    split_after,
    split_into,
    split_when,
    bucket,
    spy,
    sliding_window,
    repeat_last,
    adjacent,
    collapse,
    convolve,
    flatten,
    ilen,
    is_sorted,
    minmax,
    first_true,
    unique_to_each,
    unique_in_window,
    unique_everseen,
    unique_justseen,
    duplicates_everseen,
    duplicates_justseen,
    strip,
    lstrip,
    rstrip,
    nth_or_last,
    distinct_permutations,
    distinct_combinations,
    circular_shifts,
    partitions,
    set_partitions,
    product_index,
    combination_index,
    permutation_index,
    powerset,
    nth_product,
    nth_permutation,
    nth_combination,
    always_iterable,
    always_reversible,
    countable,
    consumer,
    with_iter,
    iter_except,
    locate,
    rlocate,
    replace,
    numeric_range,
    iterate,
    consume,
)

from functools import (
    reduce
)
