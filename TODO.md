[===] Render all lindworm files in project
[== ] Atom syntax formatting
[   ] Fix how lambdas and compositions and probably everything coming as well have to be parenthesized
[   ] Speed!
[   ] Nested lambdas don't work
[   ] Balanced brackets for nested lambdas: add second rule
[   ] Multiline comments with ###
[   ] On, Yes, Off, No, unless, contains, over

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


Result Err Ok

a contains b -> b in a
func over [1, 2, 3] -> map(func, [1, 2, 3])

unless a == 1:
    print(a)

unless ...: -> if not (...):
