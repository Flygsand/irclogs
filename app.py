# -*- coding: utf-8 -*-

import traceback
from irclogs import highlight
from irclogs.utils import config, http

class App(object):

    def __init__(self, config):
        self.config = config

    def __call__(self, env, respond):

        file = self.config.log_path + env['PATH_INFO']

        try:
            output = highlight(file, **self.config)

            respond('200 OK', [('Content-Type', 'text/html; charset=%s' % str(self.config.html_encoding))])
            yield output

        except Exception, e:
            respond(http.error_to_status(e), [('Content-Type', 'text/plain')])
            yield traceback.format_exc()

app = App(config.load_file('./config.json'))

if __name__ == '__main__':
    from paste import reloader, urlparser, cascade
    reloader.install()

    assets = urlparser.StaticURLParser('./public')

    from wsgiref import simple_server
    simple_server.make_server('', 8080, cascade.Cascade([assets, app])).serve_forever()
