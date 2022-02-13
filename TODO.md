[===] Render all lindworm files in project
[===] Atom syntax formatting
[===] Multiline comments with ###
[===] (On, Yes, Off, No, done: over, contains, unless, isnt)
[   ] Fix how lambdas and compositions and probably everything coming as well have to be parenthesized
[   ] Speed!
[   ] Nested lambdas don't work
[   ] Balanced brackets for nested lambdas: add second rule
[   ] Result


# Potential error implementation
    Result Err Ok

    item = Err("hello world")
    a = (unwrap expensive()) + 10

    __temporary = expensive()
    if __temporary.is_err():
        return __temporary.unwrap()

    a = (__temporary.unwrap()) + 10

    __temporary = expensive()
    if __temporary.is_err():
        return __temporary.unwrap()

    [LINE LEFT] (__temporary.unwrap()) [LINE RIGHT]
