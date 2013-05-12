import re
from pygments import formatters
from irclogs.utils import html

class HtmlFormatter(formatters.HtmlFormatter):

    def _format_lines(self, tokensource):
        for t, line in formatters.HtmlFormatter._format_lines(self, tokensource):
            if t == 1:
                yield 1, html.urlize(line)
            else:
                yield 0, line