import dagger.mag_calibration as mag_calibration
import unittest
from unittest.mock import Mock


class TestMagCalibration(unittest.TestCase):
    msg_length = 0
    msg_code = 206

    def test_mag_calibration(self):
        connection = Mock()
        mag_cal = mag_calibration.MagCalibration(connection)
        mag_cal.mag_calibartion()
        packet = connection.send.call_args.args[0]
        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestMagCalibration.msg_length
        assert packet[4] == TestMagCalibration.msg_code
