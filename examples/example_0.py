import lindworm

# ===| BEGIN LINDWORM METADATA |===
# uid: '00df1182784733d4ef75d13677ca9072'
# compiler:
#     name: 'sigurd'
#     version: '0.1.0'
# compilation_time: '02/12/2022, 04:04:39'
# dialect: 'lindworm'
# ===| END LINDWORM METADATA |===

import operator as op


greeting = None
greeter = (lambda _=None: print(f"So I just wanted to say, {_}"))

# None coalescing.
greeter(greeting)
greeter((greeting if greeting is not None else "Hello world!"))

# Shorthand composition.
maplist = lindworm.compose(map,  list, True, 0)

# Shorthand lambdas.
hi = 5
print(maplist((lambda _=None: (_ + 10 + hi + 30)), range(10)))
print(maplist((lambda _=None: (_ + 10)), range(10)))
print(maplist((lambda _=None: _ + 2), range(2)))

# Currying
a = lindworm.curry(op.add, *[10])(20)
print(a)

add_ten_and_print = (lindworm.compose(
    (lindworm.curry(op.add, *[10])), print, True, 0))
add_ten_and_print(13)
