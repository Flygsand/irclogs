import re
from pygments import formatters
from irclogs.utils import html

HEADER=u"""<?xml version="1.0" encoding="%(encoding)s"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>%(title)s</title>
<meta http-equiv="Content-Type" content="text/html; charset=%(encoding)s" />
<link rel="stylesheet" type="text/css" media="all" href="https://fonts.googleapis.com/css?family=Inconsolata:400,700" />
<link rel="stylesheet" type="text/css" media="screen" href="%(cssfile)s" />
</head>
<body>
<h2>%(title)s</h2>
"""

FOOTER=u"""
</body>
</html>
"""

class HtmlFormatter(formatters.HtmlFormatter):

    def __init__(self, **options):
        opts = { k: v for k, v in options.iteritems() if k not in ['full', 'cssfile', 'noclobber_cssfile'] }
        formatters.HtmlFormatter.__init__(self, **opts)
        self.header = HEADER % {
            'encoding': self.encoding, 
            'title': self.title, 
            'cssfile': self._decodeifneeded(options.get('cssfile', ''))
        }
        self.footer = FOOTER

    def wrap(self, source, outfile):

        for line in self.header.split('\n'):
            yield 0, line

        for tup in formatters.HtmlFormatter.wrap(self, source, outfile):
            yield tup

        for line in self.footer.split('\n'):
            yield 0, line

    def _format_lines(self, source):

        for t, line in formatters.HtmlFormatter._format_lines(self, source):
            if t == 1:
                yield 1, html.urlize(line)
            else:
                yield 0, line
