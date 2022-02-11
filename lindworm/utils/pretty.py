import alive_progress
import io
import sys
import colorama
import numpy as np

colorama.init()


class indent:
    def __init__(self, char=" " * 4, vspace=0):
        self.char = char
        self.buffer = io.StringIO()
        self.vspace = vspace

    def __enter__(self):
        sys.stdout = self.buffer

    def __exit__(self, *args):
        sys.stdout = sys.__stdout__
        for _ in range(self.vspace):
            print()
        self.buffer.seek(0)
        lines = self.buffer.getvalue().splitlines()
        self.buffer.close()
        print("\n".join(map(self.char.__add__, lines)))
        for _ in range(self.vspace):
            print()


def polite_warning(warning: str):
    print(f"{colorama.Fore.YELLOW}Warning: {warning} {colorama.Style.RESET_ALL}")


def polite_success(notice: str):
    print(f"{colorama.Fore.GREEN}Success: {notice} {colorama.Style.RESET_ALL}")


def polite_error(error: str, *, code: int = 1):
    print(f"{colorama.Fore.RED}Fatal: {error} {colorama.Style.RESET_ALL}")
    exit(code)


def pretty_table(table, *, spacer="  ", title=None):
    tb = []
    for column in zip(*table):
        maxwidth = max(map(lambda x: len(str(x)), column))
        tb.append(list(map(lambda x: str(x).ljust(maxwidth), column)))

    if title is not None:
        title += "\n" + len(title) * "=" + "\n"
    else:
        title = ""
    return title + "\n".join(spacer.join(i) for i in zip(*tb))


def progressbar_iterator(it):
    return alive_progress.alive_it(it, theme="smooth")


def format_si(number: float, *, significant_digits: int = 3, long: bool = False):
    """Format a number using SI prefixes.

    The prefix is chosen such that the number before the prefix is 1 < x < 1000."""

    # From https://gist.github.com/ignamv/1dde19d5a15f4562c86fade74ded2f7e.
    if number == 0:
        return '0 '

    if long:
        prefixes = ["atto", "femto", "pico", "nano", "micro", "milli", "", "kilo", "mega", "giga", "tera", "peta", "exa"]
    else:
        prefixes = [*'afpnμm', '', *'kMGTPE']

    multipliers = 10. ** np.arange(-18, 19, 3)
    inv_multipliers = 10. ** (-np.arange(-18, 19, 3))
    abs_number = abs(number)
    index = np.searchsorted(multipliers, abs_number) - 1
    prefix = prefixes[index]
    number *= inv_multipliers[index]
    abs_number = inv_multipliers[index] * abs_number

    if (abs_number > 1000 or abs_number < 1) and (index == -1 or index == len(multipliers) - 1):
        format_ = '{:.3e} '
        number *= multipliers[index]
    else:
        if abs_number < 10:
            digits_before_comma = 1
        elif abs_number < 100:
            digits_before_comma = 2
        else:
            digits_before_comma = 3
        decimals = max(0, significant_digits - digits_before_comma)
        fmt = '{:.' + str(decimals) + 'f} {}'

    return fmt.format(number, prefix)
