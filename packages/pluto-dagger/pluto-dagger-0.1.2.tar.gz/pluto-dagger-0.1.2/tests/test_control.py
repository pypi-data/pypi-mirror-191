import dagger
import dagger.control as control
import unittest
from unittest.mock import Mock


class TestPlutoControl(unittest.TestCase):
    def test_inheritance(self):
        connection = Mock()
        object = control.PlutoControl(connection)
        assert issubclass(type(object), dagger.SetRawRC)
        assert issubclass(type(object), dagger.SetCommand)
