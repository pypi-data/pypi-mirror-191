import dagger.acc_calibration as acc_calibration
import unittest
from unittest.mock import Mock


class TestAccCalibration(unittest.TestCase):
    msg_length = 0
    msg_code = 205

    def test_acc_calibration(self):
        connection = Mock()
        acc_cal = acc_calibration.AccCalibration(connection)
        acc_cal.acc_calibartion()
        packet = connection.send.call_args.args[0]
        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestAccCalibration.msg_length
        assert packet[4] == TestAccCalibration.msg_code
