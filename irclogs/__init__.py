import gzip
from pygments import highlight as pygment
from pygments.lexers import IrcLogsLexer
from irclogs.formatters import HtmlFormatter
from irclogs.utils import path

def highlight(file, **options):

    f = gzip.open(file, 'rb')
    code = ''

    try:
        
        with f:
            code = f.read()    

    except IOError, e:

        with open(file) as f:
            code = f.read()

    finally:
        lexer = IrcLogsLexer(encoding=options['log_encoding'])
        formatter = HtmlFormatter(encoding=options['html_encoding'], title=options.get('title', '%s') % path.basename(file), cssfile='/stylesheets/style.css')
        return pygment(code, lexer, formatter)