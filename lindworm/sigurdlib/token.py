import dataclasses as dc
import io
import tokenize

from .constants import constants


@dc.dataclass(eq=True, unsafe_hash=True)
class SimpleToken:
    exact_type: int
    string: str
    indent: int

    def __repr__(self):
        return f"<{type(self).__qualname__} {self.string!r} {constants.tok_name[self.exact_type]} (indent={self.indent})>"

    @property
    def type(self):
        return self.exact_type

    @classmethod
    def tokenize(cls, s):
        tokenization_stream = tokenize.tokenize(io.BytesIO(s).readline)
        item = cls.from_incomplete_stream(tokenization_stream)
        return item

    @classmethod
    def from_incomplete_stream(cls, stream):
        prev_item = None
        prev_yielded = None

        INDENT_SIZE = 4
        indent = 0

        for item in stream:
            diff_indent = (item.exact_type == tokenize.INDENT) - (item.exact_type == tokenize.DEDENT)
            indent += diff_indent
            if diff_indent:
                if prev_yielded:
                    prev_yielded.indent += diff_indent
                continue

            if item.exact_type in {tokenize.ENCODING, tokenize.ENDMARKER}:
                continue

            if prev_item and prev_item != item:
                space_type = constants.WHITESPACE
                newlines = (item.start[0] - prev_item.end[0])
                spaces = (item.start[1] - prev_item.end[1])

                if spaces and not newlines:
                    prev_yielded = cls(space_type, " " * spaces, indent)
                    yield prev_yielded

            prev_yielded = cls(constants.from_tokenize(item.exact_type), item.string, indent)
            yield prev_yielded
            prev_item = item

        return
