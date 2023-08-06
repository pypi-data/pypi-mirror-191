from ._meta import VERSION as __version__
from .peck import peck
__doc__ = """
Scan text for what looks like URI, ID or keyword

See peck() for details.

You can also use this module as CLI:

    python3 -m uripecker PATTERN_FILE [SOURCE_FILE]

where PATTERN_FILE must consist of lines in this
format:

    KEY = VALUE

If SOURCE_FILE is omitted, the text is read from
standard input.
"""
