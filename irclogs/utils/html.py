import re
from itertools import imap
from irclogs.utils import encoding

try:
    from urllib.parse import quote, urlsplit, urlunsplit
except ImportError:
    from urllib import quote
    from urlparse import urlsplit, urlunsplit

_WRAPPING_PUNCTUATION = [(r'\(', r'\)'), (r'<', '>'), (r'\[', r'\]'), (r'&lt;', r'&gt;'), (r'<\w+>', r'<\/\w+>')]
_TRAILING_PUNCTUATION = [r'\.', r',', r':', r';', r'\.\)', r'\)', r'\>', r'\]']

_unquoted_percents_re = re.compile(r'%(?![0-9A-Fa-f]{2})')
_word_split_re = re.compile(r'(\s+)')
_simple_url_re = re.compile(r'^https?://\[?\w', re.IGNORECASE)
_simple_url_2_re = re.compile(r'^www\.|^(?!http)\w[^@]+\.(com|edu|gov|int|mil|net|org)$', re.IGNORECASE)

def smart_urlquote(url):
    try:
        scheme, netloc, path, query, fragment = urlsplit(url)
        try:
            netloc = netloc.encode('idna').decode('ascii')
        except UnicodeError:
            pass
        else:
            url = urlunsplit((scheme, netloc, path, query, fragment))
    except ValueError:
        pass

    if '%' not in url or _unquoted_percents_re.search(url):
        url = quote(encoding.force_bytes(url), safe=b'!*\'();:@&=+$,/?#[]~')

    return encoding.force_text(url)

def urlize(text):
    words = _word_split_re.split(encoding.force_text(text))

    opening_re = lambda s: re.compile('(^%s)' % s)
    closing_re = lambda s: re.compile('(%s$)' % s)

    for i, word in enumerate(words):
        match = None
        if '.' in word or '@' in word or ':' in word:
            lead, middle, trail = '', word, ''
            
            for opening, closing in _WRAPPING_PUNCTUATION:
                op_m = opening_re(opening).split(middle)
                middle = op_m[-1]
                if len(op_m) > 1:
                    lead = lead + op_m[1]

                clo_m = closing_re(closing).split(middle)
                opening_count = len(re.findall(opening, middle))
                closing_count = len(re.findall(closing, middle))
                if closing_count == opening_count + 1:
                    middle = clo_m[0]
                    if len(clo_m) > 1:
                        trail = clo_m[1] + trail

            for punctuation in _TRAILING_PUNCTUATION:
                m = closing_re(punctuation).split(middle)
                middle = m[0]
                if len(m) > 1:
                    trail = m[1] + trail

            url = None
            if _simple_url_re.match(middle):
                url = smart_urlquote(middle)
            elif _simple_url_2_re.match(middle):
                url = smart_urlquote('http://%s' % middle)

            if url:
                middle = '<a target="_blank" href="%s">%s</a>' % (url, middle)
                words[i] = '%s%s%s' % (lead, middle, trail)
            else:
                words[i] = word

    return ''.join(words)