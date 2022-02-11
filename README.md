# Lindworm

A personal extension of Python inspired by Coconut.

## New operators

| Operator            | Name                      | Equivalent python syntax                        | Starrable      | Requires parentheses | Implemented |
| :------------------ | :------------------------ | :---------------------------------------------- | :------------- | :------------------- | :---------: |
| `-> (expression)`   | `lambda`                  | `lambda _=None: (expression)`                   | Yes (goal: No) | Yes (goal: No)       |      ✓      |
| `a ?? b`            | `None-coalesce`           | `a if a is not None else b`                     | Yes (goal: No) | Yes (goal: No)       |      ✓      |
| `a?[b]`             | `None-coalesce index`     | `a[b] if a is not None else None`               | Yes (goal: No) | Yes (goal: No)       |      ✓      |
| `a?.b`              | `None-coalesce attribute` | `a.b if a is not None else None`                | Yes (goal: No) | Yes (goal: No)       |      ✓      |
| `a?(b)`             | `None-coalesce call`      | `a(b) if a is not None else None`               | Yes (goal: No) | Yes (goal: No)       |      ✓      |
| `a ??= b`           | `None-coalesce equals`    | `a = a if a is not None else b`                 | Yes (goal: No) | Yes (goal: No)       |      ✓      |
| `f .. g`, `f ..> g` | `forwards compose`        | `lambda *args, **kwargs: g(f(*args, **kwargs))` | Yes (goal: No) | Yes (goal: No)       |      ✓      |
| `g <.. f`           | `backwards compose`       | `lambda *args, **kwargs: f(g(*args, **kwargs))` | Yes (goal: No) | Yes (goal: No)       |             |
| `a \|> f`           | `forwards pipe`           | `a(b)`                                          | Yes (goal: No) | Yes (goal: No)       |      ✓      |
| `f <\| a`           | `backwards pipe`          | `b(a)`                                          | Yes (goal: No) | Yes (goal: No)       |             |
| `a :: b`            | `chain`                   | `itertools.chain(a, b)`                         | Yes (goal: No) | Yes (goal: No)       |             |

## Operator currying

| Syntax            | Equivalent python syntax                  | Implemented |
| :---------------- | :---------------------------------------- | :---------: |
| `+$`, `*$`, `::$` | `op.add`, `op.mul`, `itertools.chain` ... |             |

## New functions and classes

| Syntax           | Equivalent python syntax                              | Implemented | Notes                                   |
| :--------------- | :---------------------------------------------------- | :---------: | :-------------------------------------- |
| `foldr(f, a, b)` | `lambda f, a, b: functools.reduce(f, a, b)`           |             |                                         |
| `foldl(f, a, b)` | `lambda f, a, b: functools.reduce(f, reversed(a), b)` |             |                                         |
| `foldl(f, a, b)` | `lambda f, a, b: functools.reduce(f, reversed(a), b)` |             |                                         |
| `Result`         |                                                       |             | Like Rust's `Result`.                   |
| `Ok`             |                                                       |             | Like Rust's `Ok`. Subclasses `Result`.  |
| `Err`            |                                                       |             | Like Rust's `Err`. Subclasses `Result`. |

## Misc syntax

| Syntax | Name         | Equivalent python syntax | Implemented |
| :----- | :----------- | :----------------------- | :---------: |
| `fs{}` | `frozenset`  | `frozenset`              |             |
| `f{}`  | `frozendict` | `frozendict`             |             |
| `s{}`  | `set`        | `set`                    |             |
| `n[]`  | `array`      | `numpy.array`            |      ✓      |

### Starrability

Starrable operators can have up to two stars placed inside of them to use Python's iterator and dictionary unpackings. For example:

    [10, 20, 30] |*> print  # Equivalent to print(*[10, 20, 30])
    [11, 12] |*> +$
