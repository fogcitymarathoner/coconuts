
import cherrypy
import tenjin
import json
from tenjin.helpers import *
from data import StreamJsonCalculator

from settings import FLIGHT_PATHS_FILE_JSON

with open(FLIGHT_PATHS_FILE_JSON) as json_file:
    raw_data = json.load(json_file)
calculator = StreamJsonCalculator(raw_data)
class Root(object):
    @cherrypy.expose
    def index(self, dist=None):
        if dist is None:

            engine = tenjin.Engine(path=['views'], layout='_layout.pyhtml')
            ## context data
            context = {
                'title': 'Coconuts',
                'calculator': calculator,
            }
            ## render template with context data
            html = engine.render('empty_page.pyhtml', context)
            return html
        else:

            engine = tenjin.Engine(path=['views'])
            ## context data
            context = {
                'title': 'Coconuts',
                'calculator': calculator,
                'dist': int(dist)
            }
            ## render template with context data
            html = engine.render('page.pyhtml', context)
            return html

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_port': 8092,
        'tools.proxy.on': True,
        'tools.proxy.base': 'http://fogtest.com/coconuts',
        'tools.encode.encoding': "utf-8",
    })
    cherrypy.quickstart(Root(), '/coconuts')
