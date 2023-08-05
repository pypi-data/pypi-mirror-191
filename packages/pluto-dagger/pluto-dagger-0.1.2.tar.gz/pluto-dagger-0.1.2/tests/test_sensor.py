import dagger
import dagger.sensor as sensor
import unittest
from unittest.mock import Mock


class TestPlutoControl(unittest.TestCase):
    def test_inheritance(self):
        connection = Mock()
        object = sensor.PlutoSensor(connection)
        assert issubclass(type(object), dagger.Altitude)
        assert issubclass(type(object), dagger.AccCalibration)
        assert issubclass(type(object), dagger.MagCalibration)
        assert issubclass(type(object), dagger.RawIMU)
