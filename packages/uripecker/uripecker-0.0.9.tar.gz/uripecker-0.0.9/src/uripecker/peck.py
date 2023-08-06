import itertools
import re
import urllib.parse

import neaty.log as LOG


class Candidate:

    def __init__(self, kw, query):
        self.kw = kw
        self.query = query

    def __repr__(self):
        return f'Candidate(kw={self.kw!r},query={self.query!r})'


def filter_exps(text):
    """
    Hack out expressions like bug = 123 out of the text
    """
    regex = r'\b([a-zA-Z][a-zA-Z0-9_]*)\s*=\s*([a-zA-Z0-9][a-zA-Z0-9_#-]*)\b'
    for match in re.finditer(regex, text):
        yield Candidate(*match.groups())


def filter_ids(text):
    """
    Hack out doer-like id's (ID#123) out of the text
    """
    regex = r'\b([a-zA-Z][a-zA-Z0-9_]*)#([a-zA-Z0-9][a-zA-Z0-9_#-]*)\b'
    for match in re.finditer(regex, text):
        yield Candidate(*match.groups())


def filter_kws(text):
    """
    Hack out lines that look like kw expressions (word space text)

    Eg. 'wiki hello world'
    """
    regex = r'^\s*([a-zA-Z][a-zA-Z_]*)\s+([^=].*)'
    for match in re.finditer(regex, text, flags=re.M):
        yield Candidate(*match.groups())


def filter_tags(text):
    """
    Hack out lines that look like kw expressions (word space text)

    Eg. 'wiki hello world'
    """
    for match in re.finditer('([a-zA-Z]+)([0-9]+)', text):
        yield Candidate(*match.groups())


def filter_uris(text):
    """
    Hack URIs out of the text.

    Uses URL parser regex Found as SO answer[1] and adapted to include
    comments from the original Imme's gist[2].

      [1]: https://stackoverflow.com/a/30408189/835945
      [2]: https://gist.github.com/imme-emosol/731338/810d83626a6d79f40a251f250ed4625cac0e731f
    """
    regex = (
        r'\b'
        + (
            r'(?:(?:https?|ftp)://)'     # protocol identifier
            r'(?:\S+(?::\S*)?@)?'     # user:pass authentication
        )
        + r'(?:'
        + (
            (
                r'(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])'
                r'(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}'
                r'(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))'
            )   # IP address dotted notation octets
            + r'|'
            + (
                (
                    r'(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)'
                )   # host name
                + (
                    r'(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*'
                )   # domain name
                + (
                    r'(?:\.(?:[a-z\u00a1-\uffff]{2,}))'
                )   # TLD identifier
            )
            + r'|'
            + (
                r'(?:localhost)'
            )   # "localhost"
        )
        + r')'
        + (
            r'(?::\d{2,5})?'
        )   # port number
        + (
            r'(?:/[^\s>]*)?'
        )   # resource path
    )
    for uri in re.findall(regex, text):
        yield uri.rstrip(').>')


class CiDict(dict):

    @classmethod
    def from_arg(cls, arg):
        seen = {}
        for k in arg.keys():
            lk = k.lower()
            if lk in seen:
                raise ValueError(f"duplicate key: {k!r} vs. {seen[lk]!r}")
            seen[lk] = k
        return cls(arg)

    def get(self, key, default=None):
        """
        Imitate dict.get() but with case-insensitive key comparison
        """
        for k, v in self.items():
            if k.lower() == key.lower():
                return v
        return default


def _deref(candidates, pmap):
    """
    Turn query (like "g hello" for google) to URI
    """
    for c in candidates:
        LOG.debug('_deref():c.kw=%r' % c.kw)
        LOG.debug('_deref():c.query=%r' % c.query)
        pattern = pmap.get(c.kw)
        LOG.debug('_deref():c.pattern=%r' % pattern)
        if pattern:
            yield pattern % _urlquote(c.query)


def _urlquote(text):
    """
    URL-quote *text*
    """
    LOG.debug('_urlquote():text=%r' % text)
    return urllib.parse.quote_plus(text)
    # original s-b-uripecker forced LC_ALL=en_US.UTF-8 for
    # the conversion and had a FIXME note:
    #
    # >    #FIXME: There should be proper way w/o touching LC_ALL


def peck(pmap, text):
    """
    Scan text for what looks like URI, ID or keyword

    Usage:
        uripecker.peck(pmap=PATTERN_MAP, text=SOURCE_TEXT)

    Search through SOURCE_TEXT and output in following order:

     1. apparent URIs,
     2. hash IDs ("bug#1234"),
     3. equal sign expressions ("bug = 1234"),
     4. "tags" ("bug1234")
     5. keyword expressions ("BUG 1234" or "g hello world"),

    all (except the first one, obviously) converted to URI using mappings
    from PATTERN_MAP file.

    Note that keyword expressions (e.g. "bug 123") work only if they start
    the line;  rest of the line is taken as query argument and URL-quoted,
    so that "g what is bmo" would work as expected (given 'g' is defined
    as Google search).

    Apply this filter to args or clipboard, and open the first, or if you
    are brave, open all URIs.

    The PATTERN_MAP is a dictionary containing query names to URI patterns,
    where query name is any string without spaces, equal sign or dot, and
    URI pattern is a string with precisely one instance of '%s'.

    For example, given this PATTERN_MAP:

        >>> PATTERN_MAP = {
        ... 'issue': 'http://gitlab.example.org/issue?id=%s',
        ... 'faq': 'http://faq.example.org/faq/%s',
        ... }

    following text

        >>> SOURCE_TEXT = '''
        ... issue = 1
        ... faq#225
        ... issue42
        ... http://other.example.com/
        ... faq 14
        ... or faq 15
        ... '''

    would return generator with following items:

        >>> found = list(peck(pmap=PATTERN_MAP, text=SOURCE_TEXT))
        >>> import pprint; pprint.pp(found, width=1)
        ['http://other.example.com/',
         'http://faq.example.org/faq/225',
         'http://gitlab.example.org/issue?id=1',
         'http://gitlab.example.org/issue?id=42',
         'http://faq.example.org/faq/14']

    Note that the URI pattern can be any kind of URI, such as ftp:// URI,
    (or any string, actually) but the '%s' is converted using HTTP URI
    quoting rules.

    Keys in PATTERN_MAP are treated as case-insensitive, so if the *pmap*
    argument contains two keys that only differ in case, ValueError is
    raised.

    Following example uses invalud PATTERN_MAP:

        >>> BAD_PATTERN_MAP = {
        ... 'issue': 'http://gitlab.example.org/issue?id=%s',
        ... 'faq': 'http://faq.example.org/faq/%s',
        ... 'FAQ': 'http://faq.other.example.org/faq/%s',
        ... }
        >>> found = list(peck(pmap=BAD_PATTERN_MAP, text=SOURCE_TEXT))
        Traceback (most recent call last):
            ...
        ValueError: duplicate key: 'FAQ' vs. 'faq'

    """
    pmap = CiDict.from_arg(pmap)
    LOG.debug('peck():pmap=%r' % pmap)
    candidates = itertools.chain(
        filter_ids(text),
        filter_exps(text),
        filter_tags(text),
        filter_kws(text),
    )
    LOG.debug('peck():candidates=%r' % candidates)
    return itertools.chain(
        filter_uris(text),
        _deref(candidates, pmap)
    )
