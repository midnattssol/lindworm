# Lindworm

A personal extension of Python inspired by Coconut.

## New operators

| Operator            | Name                      | Equivalent python syntax                        | Max stars | Requires parentheses | Implemented |
| :------------------ | :------------------------ | :---------------------------------------------- | :-------- | :------------------- | :---------: |
| `-> (expression)`   | `lambda`                  | `lambda _=None: (expression)`                   | 0         | Yes (goal: No)       |      ✓      |
| `a ?? b`            | `None-coalesce`           | `a if a is not None else b`                     | 0         | No                   |      ✓      |
| `a?[b]`             | `None-coalesce index`     | `a[b] if a is not None else None`               | 0         | Yes (goal: No)       |      ✓      |
| `a?.b`              | `None-coalesce attribute` | `a.b if a is not None else None`                | 0         | Yes (goal: No)       |      ✓      |
| `a?(b)`             | `None-coalesce call`      | `a(b) if a is not None else None`               | 0         | Yes (goal: No)       |      ✓      |
| `a ??= b`           | `None-coalesce equals`    | `a = a if a is not None else b`                 | 0         | No                   |      ✓      |
| `f .. g`, `f ..> g` | `forwards compose`        | `lambda *args, **kwargs: g(f(*args, **kwargs))` | 2         | Yes (goal: No)       |      ✓      |
| `g <.. f`           | `backwards compose`       | `lambda *args, **kwargs: f(g(*args, **kwargs))` | 2         | Yes (goal: No)       |      ✓      |
| `a \|> f`           | `forwards pipe`           | `a(b)`                                          | 2         | Yes (goal: No)       |      ✓      |
| `f <\| a`           | `backwards pipe`          | `b(a)`                                          | 2         | Yes (goal: No)       |      ✓      |
| `a :: b`            | `chain`                   | `itertools.chain(a, b)`                         | 1         | No                   |      ✓      |
| `a over b`          | `over`                    | `map(a, b)`                                     | 1         | No                   |      ✓      |
| `a contains b`      | `contains`                | `b in a`                                        | 1         | No                   |      ✓      |
| `a isnt b`          | `isnt`                    | `a is not b`                                    | 1         | No                   |      ✓      |

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

| Syntax      | Name         | Equivalent python syntax | Implemented |
| :---------- | :----------- | :----------------------- | :---------: |
| `fs{}`      | `frozenset`  | `frozenset`              |             |
| `f{}`       | `frozendict` | `frozendict`             |             |
| `s{}`       | `set`        | `set`                    |             |
| `n[]`       | `array`      | `numpy.array`            |      ✓      |
| `On`, `Yes` | `On`, `Yes`  | `True`                   |      ✓      |
| `Off`, `No` | `Off`, `No`  | `False`                  |      ✓      |
| `unless b:` | `unless`     | `if not b:`              |      ✓      |

### Starrability

Starrable operators can have up to two stars placed inside of them to use Python's iterator and dictionary unpackings. For example:

    [10, 20, 30] |*> print  # Equivalent to print(*[10, 20, 30])
    [11, 12] |*> +$
