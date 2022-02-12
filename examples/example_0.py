import lindworm
from lindworm.builtins import *

# ===| BEGIN LINDWORM METADATA |===
# uid: '69e9f65c75a7659c8437aa3832ff9cdb'
# compiler:
#     name: 'sigurd'
#     version: '0.1.0'
# compilation_time: '02/12/2022, 19:11:58'
# dialect: 'lindworm'
# ===| END LINDWORM METADATA |===

import operator as op

# Shorthand lambdas.
greeter = (lambda _=None: print("So I just wanted to say" + _))

# None coalescing.
greeting = None
greeter(greeting)
greeter((greeting if greeting is not None else "Hello world!"))

# Function composition.
maplist = lindworm.compose(map,  list, True, 0)

# Shorthand lambdas.
hi = 5
print(maplist((lambda _=None: _ + 2), range(2)))

# Function currying
ten_adder = lindworm.curry(op.add, *[20])
add_ten_and_print = (lindworm.compose(ten_adder, print, True, 0))
add_ten_and_print(13)

# Operator currying
multiply = OPERATORS['*']
print(multiply(10, 20))
print(10 * 20)


print(reduce([10, 20, 30], OPERATORS['*'], 1))
