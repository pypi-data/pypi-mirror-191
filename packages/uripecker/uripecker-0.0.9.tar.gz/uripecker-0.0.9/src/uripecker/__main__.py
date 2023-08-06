import sys

import neaty.log as LOG

from .peck import peck


class UsageError(RuntimeError):
    pass


class AppError(RuntimeError):
    pass


def parse_mapfile(path):
    """
    Parse file at *path* into dict usable as 'pmap' for peck()

    See parse_maptext() for details about file format.
    """
    return parse_maptext(slurp(path))


def parse_maptext(text):
    """
    Parse text with pattern map into dict usable as 'pmap' for peck().

    Each line of the text must have following format:

        KEY = VALUE

    where spaces around key and value as well as empty lines and
    lines starting with '#' are ignored.
    """
    out = {}
    for line in text.split('\n'):
        LOG.debug('parse_maptext():line=%r' % line)
        if line:
            if line.lstrip()[0] == '#':
                continue
            key, value = map(
                str.strip,
                line.split('=', maxsplit=1)
            )
            if '%s' not in value:
                warn(f"ignoring pattern without '%s': {key} = {value}")
                continue
            out[key] = value
    return out


def slurp(path):
    """
    Read text at *path*, return it all
    """
    with open(path) as fh:
        return fh.read()


def warn(msg, nopfx=False):
    pfx = '' if nopfx else 'uripecker:'
    if type(msg) is list:
        for line in msg:
            print(pfx + line, file=sys.stderr)
    else:
        print(pfx + msg, file=sys.stderr)


def usage(msg=None):
    lines = [
        "usage: python3 -m uripecker PATTERN_MAP_FILE [SOURCE_TEXT_FILE]",
        "usage: python3 -m uripecker --help"
    ]
    if msg:
        lines.append('')
        lines.append(msg)
    warn(lines, nopfx=True)
    sys.exit(2)


_HELP_TEXT = """
Scan text for what looks like URI, ID or keyword expression.

Usage:
    python3 -m uripecker PATTERN_MAP_FILE [SOURCE_TEXT_FILE]

uripecker will look for several known forms in SOURCE_TEXT_FILE:

 1. apparent URIs,
 2. hash IDs (`bug#1234"`),
 3. equal sign expressions (`bug = 1234`),
 4. "tags" (`bug1234`)
 5. keyword expressions (`bug 1234` or `g hello world`),

Once found, uripecker will try to translate the above forms
URI's according to patterns in PATTERN_MAP_FILE, and print
the results the order as above.  (I.e. first all apparent
URI's in the order they appeared in SOURCE_TEXT_FILE, then
all successfully translated hash ID's in the order found in
SOURCE_TEXT_FILE, etc.)

If SOURCE_TEXT_FILE is omitted, the text is read from
standard input.

PATTERN_MAP_FILE must consist of lines in this format:

    KEY = VALUE

where any KEY must consist only of letters, numbers, and
underscore.  VALUE must be a string -- typically a URI
pattern -- containing a single instance of `%s`.

KEYs are case-insensitive, so a map containing two KEYs
that only differ in letter case is not a valid map.

Empty lines, lines starting with `#`, and whitespace (except
whitespace embedded within VALUE) is ignored.

See also uripecker.peck() for details and examples.
""".strip()


def help_():
    print(_HELP_TEXT)
    sys.exit(0)


def main():
    """
    Main CLI entrypoint.
    """
    if len(sys.argv) == 1:
        usage("missing PATTERN_MAP_FILE")
    if len(sys.argv) == 2 and sys.argv[1] == '--help':
        help_()
    if len(sys.argv) == 2:
        pmap = parse_mapfile(sys.argv[1])
        text = sys.stdin.read()
    elif len(sys.argv) == 3:
        pmap = parse_mapfile(sys.argv[1])
        text = slurp(sys.argv[2])
    else:
        usage("extra parameters!")
    for line in peck(pmap=pmap, text=text):
        print(line)


if __name__ == '__main__':
    main()
