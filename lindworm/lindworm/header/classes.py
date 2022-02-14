import dataclasses as dc
import typing as t

import more_itertools as mit


@dc.dataclass
class LindwormIteratorSlicer:
    """A class for slicing iterators."""

    iterator: t.Iterator

    def __getitem__(self, index):
        if isinstance(index, int):
            for _ in range(index):
                next(self.iterator)
            return next(self.iterator)
        if isinstance(index, slice):
            return mit.islice_extended(
                self.iterator, index.start, index.stop, index.step
            )

        raise TypeError(
            f"{type(self).__qualname__} indices must be integers or slices, not {type(index).__qualname__}"
        )
