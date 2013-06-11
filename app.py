# -*- coding: utf-8 -*-

import traceback
import gzip
from pygments import highlight
from pygments.lexers import IrcLogsLexer
from irclogs.formatters import HtmlFormatter
from irclogs.utils import config, http, path

class App(object):

    def __init__(self, config):
        self.config = config

    def __call__(self, env, respond):

        file = self.config.log_path + env['PATH_INFO']

        try:
            output = self.highlight(file)

            respond('200 OK', [('Content-Type', 'text/html; charset=%s' % str(self.config.html_encoding))])
            yield output

        except Exception, e:
            respond(http.error_to_status(e), [('Content-Type', 'text/plain')])
            yield traceback.format_exc()

    def highlight(self, file):

        f = gzip.open(file, 'rb')
        code = ''

        try:
            
            with f:
                code = f.read()    

        except IOError, e:

            with open(file) as f:
                code = f.read()

        finally:
            lexer = IrcLogsLexer(encoding=self.config.log_encoding)
            formatter = HtmlFormatter(encoding=self.config.html_encoding, title=self.config.title % path.basename(file), cssfile='/stylesheets/style.css')
            return highlight(code, lexer, formatter)


app = App(config.load_file('./config.json'))

if __name__ == '__main__':
    from paste import reloader, urlparser, cascade
    reloader.install()

    assets = urlparser.StaticURLParser('./public')

    from wsgiref import simple_server
    simple_server.make_server('', 8080, cascade.Cascade([assets, app])).serve_forever()
