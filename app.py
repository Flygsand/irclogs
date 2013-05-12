# -*- coding: utf-8 -*-

import traceback
import gzip
from os import path
from pygments import highlight
from pygments.lexers import IrcLogsLexer
from irclogs.formatters import HtmlFormatter
from irclogs.utils import config, http

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
            formatter = HtmlFormatter(encoding=self.config.html_encoding, full=True, title=self.config.title % path.basename(file), cssfile='./stylesheets/style.css', noclobber_cssfile=True)
            return highlight(code, lexer, formatter)


app = App(config.load_file('./config.json'))

if __name__ == '__main__':
    from paste import reloader
    reloader.install()

    from wsgiref import simple_server
    simple_server.make_server('', 8080, app).serve_forever()
