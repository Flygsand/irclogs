# -*- coding: utf-8 -*-

import gzip
from os import path
from pygments import highlight
from pygments.lexers import IrcLogsLexer
from pygments.formatters import HtmlFormatter
from configuration import load_config
from http import error_to_status

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
            respond(error_to_status(e), [('Content-Type', 'text/plain')])
            yield str(e)

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


app = App(load_config('./config.json'))
