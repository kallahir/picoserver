from picoserver import PicoServer

def test_default_init():
    s = PicoServer()
    assert s._host == '0.0.0.0', 'unexpected host name'
    assert s._port == 80, 'unexpected port value'
    assert s._buffer_length == 4096, 'unexpected buffer length'

def test_custom_init():
    host, port, buffer_length = '192.168.1.1', 8088, 1024
    s = PicoServer(host=host, port=port, buffer_length=buffer_length)
    assert s._host == host, 'unexpected host name'
    assert s._port == port, 'unexpected port value'
    assert s._buffer_length == buffer_length, 'unexpected buffer length'
