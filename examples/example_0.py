import lindworm

# ===| BEGIN LINDWORM METADATA |===
# uid: '7ebca463f9ad68e3dda41f74c3f7d5a1'
# compiler:
#     name: 'sigurd'
#     version: '0.0.1'
# compilation_time: '02/11/2022, 01:29:39'
# dialect: 'lindworm'
# ===| END LINDWORM METADATA |===

import operator as op


greeting = None
greeter = (lambda _=None: print(f"So I just wanted to say, {_}"))

# None coalescing.
greeter(greeting)
greeter(greeting  if greeting  is not None else  "Hello world!")

# Shorthand composition.
maplist =lindworm.compose( map ,  list, True)

# Shorthand lambdas.
hi = 5
print(maplist((lambda _=None: (_ + 10 + hi + 30)), range(10)))
print(maplist((lambda _=None: (_ + 10)), range(10)))
print(maplist((lambda _=None: _ + 2), range(2)))

# Currying
a =lindworm.curry( op.add, *[10])(20)
print(a)

add_ten_and_print = (lindworm.compose((lindworm.curry(op.add, *[10])) ,  print, True))
add_ten_and_print(13)

