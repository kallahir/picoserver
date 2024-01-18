import json

from picoserver import PicoServer

server = PicoServer(port=8088)

@server.route('/test')
def test(request):
    server.respond(200, "application/json", json.dumps(request.args))

@server.route('/test/1')
def test1(request):
    server.respond(200, "application/json", json.dumps(request.args))

server.start()