import dagger.connect as connect
import socket
import unittest


class TestPlutoConnection(unittest.TestCase):
    def test_init(self):
        connection = connect.PlutoConnection()
        assert connection.family == socket.AF_INET
        assert connection.type == socket.SOCK_STREAM
