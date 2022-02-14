[   ] Fix how lambdas and compositions and probably everything coming as well have to be parenthesized


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
