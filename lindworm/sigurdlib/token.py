import dataclasses as dc
import io
import tokenize
import typing as t

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
    def tokenize(cls, code: bytes, **kwargs) -> t.Generator:
        """Turns code into a stream of SimpleTokens."""
        stream = tokenize.tokenize(io.BytesIO(code).readline)
        item = cls.from_incomplete_stream(stream, **kwargs)
        return item

    @classmethod
    def from_incomplete_stream(cls, stream: t.Iterable, *, indent=0) -> t.Generator:
        """Turns a tokenize.tokenize stream into a SimpleToken stream, adding whitespace tokens and removing INDENT and DEDENT tokens."""
        INDENT_SIZE = 4
        prev_item = None
        output = []

        for item in stream:
            # Skip indents and dedents and store it in each token instead.
            diff_indent = (item.exact_type == tokenize.INDENT) - \
                (item.exact_type == tokenize.DEDENT)
            indent += diff_indent
            if diff_indent:
                if output:
                    output[-1].indent += diff_indent
                continue

            # Skip encoding and end markers.
            if item.exact_type in {tokenize.ENCODING, tokenize.ENDMARKER}:
                continue

            # Adds whitespace.
            if prev_item and prev_item != item:
                newlines = (item.start[0] - prev_item.end[0])
                spaces = (item.start[1] - prev_item.end[1])

                if spaces and not newlines:
                    output.append(cls(constants.WHITESPACE, " " * spaces, indent))

            result = cls(constants.from_tokenize(item.exact_type), item.string, indent)
            output.append(result)
            prev_item = item

        return output
