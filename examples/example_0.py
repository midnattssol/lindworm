import lindworm
import lindworm.header
from lindworm.new_builtins import *

# ===| BEGIN LINDWORM METADATA |===
# uid: '38569e0e707c4a7fb9fbc698dff22d38'
# compiler:
#     name: 'sigurd'
#     version: '0.1.0'
# compilation_time: '02/12/2022, 20:09:10'
# dialect: 'lindworm'
# ===| END LINDWORM METADATA |===

"""Lindworm examples."""
import operator as op

# Shorthand lambdas.
greeter = (lambda _=None: print(f"Hello {_}!"))

# None coalescing.
greeting = None
greeter(greeting)
greeter((greeting  if greeting  is not None else  "world"))

# Function composition.
maplist =lindworm.header.compose( map ,  list, True, 0)
print(maplist((lambda _=None: _ + 2), range(2)))

# Function currying
ten_adder =lindworm.header.curry( op.add, *[20])
add_ten_and_print = (lindworm.header.compose(ten_adder ,  print, True, 0))
add_ten_and_print(13)

# Operator currying
multiply = lindworm.header.OPERATORS['*']
print(multiply(10, 20))

product = (lambda _=None: reduce(lindworm.header.OPERATORS['*'], _, 1))
print(product([10, 20, 30]))

