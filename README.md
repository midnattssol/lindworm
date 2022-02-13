# Lindworm

Lindworm is my personal extension of Python, inspired by Coconut and functional programming.  Like Coconut, all valid Python code is also Lindworm code. The package comes with a compiler, Sigurd, which transpiles it into human-readable Python code or `.pyc` code. Lindworm is suitable for writing extensions or packages which make heavy use of functional programming.

## Installation

Lindworm is on [PyPi](https://pypi.org/project/lindworm-language/), and can be installed with pip from the command line with the following command:

    pip install lindworm-language


## Examples

Lindworm comes with several new operators, as well as ways to combine them. , so it can be easily switched between. It has a high compilation speed and remains both short and relatively readable after compilation. For example:

    # Lindworm
    factorial = -> range(1, _) |> fold_left$(*$)
    print(factorial(5))


Compiles into this:

    # Compiled Python
    import lindworm
    import lindworm.header
    from lindworm.new_builtins import *

    factorial = lambda _=None: (
        lindworm.header.curry(fold_left, \*[lindworm.header.OPERATORS["*"]])(range(1, _))
    )
    print(factorial(5))


## Features

### Starrability

Starrable operators can have up to two stars placed inside of them to use Python's iterator and dictionary unpackings. For example:

    [10, 20, 30] |*> print  # Equivalent to print(*[10, 20, 30])
    [11, 12] |*> +$

### New operators

| Operator            | Name                      | Equivalent python syntax                                       | Max stars | Requires parentheses | Implemented |
| :------------------ | :------------------------ | :------------------------------------------------------------- | :-------- | :------------------- | :---------: |
| `f .. g`, `f ..> g` | `forwards compose`        | `lambda *args, **kwargs: g(f(*args, **kwargs))`                | 2         | Yes (goal: No)       |      ✓      |
| `g <.. f`           | `backwards compose`       | `lambda *args, **kwargs: f(g(*args, **kwargs))`                | 2         | Yes (goal: No)       |      ✓      |
| `a \|> f`           | `forwards pipe`           | `a(b)`                                                         | 2         | Yes (goal: No)       |      ✓      |
| `f <\| a`           | `backwards pipe`          | `b(a)`                                                         | 2         | Yes (goal: No)       |      ✓      |
| `a :: b`            | `chain`                   | `itertools.chain(a, b)`                                        | 1         | No                   |      ✓      |
| `a ::: b`           | `always-iterable chain`   | `itertools.chain(map(more_itertools.always_iterable, [a, b]))` | 0         | No                   |      ✓      |
| `->`, `λ`           | `lambda`                  | `lambda _=None: (expression)`                                  | 0         | Yes (goal: No)       |      ✓      |
| `a ?? b`            | `None-coalesce`           | `a if a is not None else b`                                    | 0         | No                   |      ✓      |
| `a?[b]`             | `None-coalesce index`     | `a[b] if a is not None else None`                              | 0         | Yes (goal: No)       |      ✓      |
| `a?.b`              | `None-coalesce attribute` | `a.b if a is not None else None`                               | 0         | Yes (goal: No)       |      ✓      |
| `a?(b)`             | `None-coalesce call`      | `a(b) if a is not None else None`                              | 0         | Yes (goal: No)       |      ✓      |
| `a ??= b`           | `None-coalesce equals`    | `a = a if a is not None else b`                                | 0         | No                   |      ✓      |
| `a over b`          | `over`                    | `map(a, b)`                                                    | 0         | No                   |      ✓      |
| `a contains b`      | `contains`                | `b in a`                                                       | 0         | No                   |      ✓      |
| `a isnt b`          | `isnt`                    | `a is not b`                                                   | 0         | No                   |      ✓      |

### Operator currying

| Syntax            | Equivalent python syntax                  | Implemented |
| :---------------- | :---------------------------------------- | :---------: |
| `+$`, `*$`, `::$` | `op.add`, `op.mul`, `itertools.chain` ... |      ✓      |

### New built-in functions and classes

The new built-ins are currently `chain`, `combinations`, `count`, `groupby`, `permutations`, `product`, `adjacent`, `always_iterable,
always_reversible`, `bucket`, `circular_shifts`, `collapse`, `combination_index`, `consume`, `consumer`, `convolve,
countable`, `distinct_combinations`, `distinct_permutations`, `duplicates_everseen,
duplicates_justseen`, `first_true`, `flatten`, `fold_left`, `fold_right`, `ilen`, `is_sorted`, `iter_except`, `iterate`, `locate`, `lstrip,
minmax`, `nth_combination`, `nth_or_last`, `nth_permutation`, `nth_product`, `numeric_range,
partitions`, `permutation_index`, `powerset`, `product_index`, `repeat_last`, `replace`, `rlocate,
rstrip`, `set_partitions`, `sliding_window`, `split_after`, `split_at`, `split_before`, `split_into,
split_when`, `spy`, `strip`, `unique_everseen`, `unique_in_window`, `unique_justseen`, `unique_to_each`, and `with_iter`.

Most of them come from `more_itertools`, `itertools`, and similar libraries. This is not a stable list though!

### Aliases

| Syntax      | Name         | Equivalent python syntax | Implemented |
| :---------- | :----------- | :----------------------- | :---------: |
| `fs{}`      | `frozenset`  | `frozenset`              |      ✓      |
| `f{}`       | `frozendict` | `frozendict`             |      ✓      |
| `s{}`       | `set`        | `set`                    |      ✓      |
| `n[]`       | `array`      | `numpy.array`            |      ✓      |
| `On`, `Yes` | `On`, `Yes`  | `True`                   |      ✓      |
| `Off`, `No` | `Off`, `No`  | `False`                  |      ✓      |

### New classes

| Syntax           | Equivalent python syntax                              | Implemented | Notes                                   |
| :--------------- | :---------------------------------------------------- | :---------: | :-------------------------------------- |
| `Result`         |                                                       |      ✓      | Like Rust's `Result`.                   |
| `Ok`             |                                                       |      ✓      | Like Rust's `Ok`. Subclasses `Result`.  |
| `Err`            |                                                       |      ✓      | Like Rust's `Err`. Subclasses `Result`. |


### Control flow

| Syntax      | Name     | Equivalent python syntax | Implemented |
| :---------- | :------- | :----------------------- | :---------: |
| `unless b:` | `unless` | `if not b:`              |      ✓      |
| `unwrap a`  | `unwrap` |                          |             |

<<<<<<< HEAD
#### Starrability

Starrable operators can have up to two stars placed inside of them to use Python's iterator and dictionary unpackings. For example:

    [10, 20, 30] |*> print  # Equivalent to print(*[10, 20, 30])
    [11, 12] |*> +$

## See also

- [Atom language highlighting for Lindworm](https://github.com/midnattssol/atom-language-lindworm)
- [Coconut](https://github.com/evhub/coconut)
=======
>>>>>>> c51cf46246acbe3cb97160eae08fdf3f44d003e0
