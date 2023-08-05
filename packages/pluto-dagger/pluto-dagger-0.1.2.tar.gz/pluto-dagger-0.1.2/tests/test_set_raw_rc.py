import dagger.set_raw_rc as set_raw_rc
import unittest
from unittest.mock import Mock


class TestSetRawRC(unittest.TestCase):
    msg_length = 16
    msg_code = 200
    roll_position = 5
    pitch_position = 7
    throttle_position = 9
    yaw_position = 11
    aux1_position = 13
    aux2_position = 15
    aux3_position = 17
    aux4_position = 19

    def test_roll(self):
        connection = Mock()
        rc = set_raw_rc.SetRawRC(connection)

        rc.set_roll(1500)
        packet = connection.send.call_args.args[0]

        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestSetRawRC.msg_length
        assert packet[4] == TestSetRawRC.msg_code
        assert (
            int.from_bytes(
                packet[TestSetRawRC.roll_position : TestSetRawRC.roll_position + 2],
                "little",
            )
            == 1500
        )

        rc.set_roll(1800)
        packet = connection.send.call_args.args[0]
        assert (
            int.from_bytes(
                packet[TestSetRawRC.roll_position : TestSetRawRC.roll_position + 2],
                "little",
            )
            == 1800
        )

        rc.set_roll(1200)
        packet = connection.send.call_args.args[0]
        assert (
            int.from_bytes(
                packet[TestSetRawRC.roll_position : TestSetRawRC.roll_position + 2],
                "little",
            )
            == 1200
        )

    def test_pitch(self):
        connection = Mock()
        rc = set_raw_rc.SetRawRC(connection)

        rc.set_pitch(1500)
        packet = connection.send.call_args.args[0]

        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestSetRawRC.msg_length
        assert packet[4] == TestSetRawRC.msg_code
        assert (
            int.from_bytes(
                packet[TestSetRawRC.pitch_position : TestSetRawRC.pitch_position + 2],
                "little",
            )
            == 1500
        )

        rc.set_pitch(1800)
        packet = connection.send.call_args.args[0]
        assert (
            int.from_bytes(
                packet[TestSetRawRC.pitch_position : TestSetRawRC.pitch_position + 2],
                "little",
            )
            == 1800
        )

        rc.set_pitch(1200)
        packet = connection.send.call_args.args[0]
        assert (
            int.from_bytes(
                packet[TestSetRawRC.pitch_position : TestSetRawRC.pitch_position + 2],
                "little",
            )
            == 1200
        )

    def test_yaw(self):
        connection = Mock()
        rc = set_raw_rc.SetRawRC(connection)

        rc.set_yaw(1500)
        packet = connection.send.call_args.args[0]

        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestSetRawRC.msg_length
        assert packet[4] == TestSetRawRC.msg_code
        assert (
            int.from_bytes(
                packet[TestSetRawRC.yaw_position : TestSetRawRC.yaw_position + 2],
                "little",
            )
            == 1500
        )

        rc.set_yaw(1800)
        packet = connection.send.call_args.args[0]
        assert (
            int.from_bytes(
                packet[TestSetRawRC.yaw_position : TestSetRawRC.yaw_position + 2],
                "little",
            )
            == 1800
        )

        rc.set_yaw(1200)
        packet = connection.send.call_args.args[0]
        assert (
            int.from_bytes(
                packet[TestSetRawRC.yaw_position : TestSetRawRC.yaw_position + 2],
                "little",
            )
            == 1200
        )

    def test_throttle(self):
        connection = Mock()
        rc = set_raw_rc.SetRawRC(connection)

        rc.set_throttle(1500)
        packet = connection.send.call_args.args[0]

        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestSetRawRC.msg_length
        assert packet[4] == TestSetRawRC.msg_code
        assert (
            int.from_bytes(
                packet[
                    TestSetRawRC.throttle_position : TestSetRawRC.throttle_position + 2
                ],
                "little",
            )
            == 1500
        )

        rc.set_throttle(1800)
        packet = connection.send.call_args.args[0]
        assert (
            int.from_bytes(
                packet[
                    TestSetRawRC.throttle_position : TestSetRawRC.throttle_position + 2
                ],
                "little",
            )
            == 1800
        )

        rc.set_throttle(1200)
        packet = connection.send.call_args.args[0]
        assert (
            int.from_bytes(
                packet[
                    TestSetRawRC.throttle_position : TestSetRawRC.throttle_position + 2
                ],
                "little",
            )
            == 1200
        )

    def test_set_maghold_mode(self):
        connection = Mock()
        rc = set_raw_rc.SetRawRC(connection)

        rc.set_maghold_mode()
        packet = connection.send.call_args.args[0]

        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestSetRawRC.msg_length
        assert packet[4] == TestSetRawRC.msg_code
        assert (
            int.from_bytes(
                packet[TestSetRawRC.aux1_position : TestSetRawRC.aux1_position + 2],
                "little",
            )
            > 900
        )
        assert (
            int.from_bytes(
                packet[TestSetRawRC.aux1_position : TestSetRawRC.aux1_position + 2],
                "little",
            )
            < 1300
        )

    def test_set_headfree_mode(self):
        connection = Mock()
        rc = set_raw_rc.SetRawRC(connection)

        rc.set_headfree_mode()
        packet = connection.send.call_args.args[0]

        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestSetRawRC.msg_length
        assert packet[4] == TestSetRawRC.msg_code
        assert (
            int.from_bytes(
                packet[TestSetRawRC.aux1_position : TestSetRawRC.aux1_position + 2],
                "little",
            )
            > 1300
        )
        assert (
            int.from_bytes(
                packet[TestSetRawRC.aux1_position : TestSetRawRC.aux1_position + 2],
                "little",
            )
            < 1700
        )

    def test_set_developer_mode(self):
        connection = Mock()
        rc = set_raw_rc.SetRawRC(connection)

        rc.set_developer_mode_on()
        packet = connection.send.call_args.args[0]

        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestSetRawRC.msg_length
        assert packet[4] == TestSetRawRC.msg_code
        assert (
            int.from_bytes(
                packet[TestSetRawRC.aux2_position : TestSetRawRC.aux2_position + 2],
                "little",
            )
            == 1500
        )

        rc.set_developer_mode_off()
        packet = connection.send.call_args.args[0]
        assert (
            int.from_bytes(
                packet[TestSetRawRC.aux2_position : TestSetRawRC.aux2_position + 2],
                "little",
            )
            != 1500
        )

    def test_set_alt_hold_mode(self):
        connection = Mock()
        rc = set_raw_rc.SetRawRC(connection)

        rc.set_alt_hold_mode()
        packet = connection.send.call_args.args[0]

        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestSetRawRC.msg_length
        assert packet[4] == TestSetRawRC.msg_code
        assert (
            int.from_bytes(
                packet[TestSetRawRC.aux3_position : TestSetRawRC.aux3_position + 2],
                "little",
            )
            > 1300
        )
        assert (
            int.from_bytes(
                packet[TestSetRawRC.aux3_position : TestSetRawRC.aux3_position + 2],
                "little",
            )
            < 1700
        )

    def test_set_throttle_free_mode(self):
        connection = Mock()
        rc = set_raw_rc.SetRawRC(connection)

        rc.set_throttle_free_mode()
        packet = connection.send.call_args.args[0]

        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestSetRawRC.msg_length
        assert packet[4] == TestSetRawRC.msg_code
        aux3_val = int.from_bytes(
            packet[TestSetRawRC.aux3_position : TestSetRawRC.aux3_position + 2],
            "little",
        )
        assert aux3_val < 1300 or aux3_val > 1700

    def test_arm_drone(self):
        connection = Mock()
        rc = set_raw_rc.SetRawRC(connection)

        rc.arm_drone()
        packet = connection.send.call_args.args[0]

        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestSetRawRC.msg_length
        assert packet[4] == TestSetRawRC.msg_code
        assert (
            int.from_bytes(
                packet[TestSetRawRC.aux4_position : TestSetRawRC.aux4_position + 2],
                "little",
            )
            > 1300
        )
        assert (
            int.from_bytes(
                packet[TestSetRawRC.aux4_position : TestSetRawRC.aux4_position + 2],
                "little",
            )
            < 1700
        )

    def test_disarm_drone(self):
        connection = Mock()
        rc = set_raw_rc.SetRawRC(connection)

        rc.disarm_drone()
        packet = connection.send.call_args.args[0]

        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestSetRawRC.msg_length
        assert packet[4] == TestSetRawRC.msg_code
        aux4_val = int.from_bytes(
            packet[TestSetRawRC.aux4_position : TestSetRawRC.aux4_position + 2],
            "little",
        )
        assert aux4_val < 1300 or aux4_val > 1700

    def test_box_arm(self):
        connection = Mock()
        rc = set_raw_rc.SetRawRC(connection)

        rc.box_arm()
        packet = connection.send.call_args.args[0]

        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestSetRawRC.msg_length
        assert packet[4] == TestSetRawRC.msg_code
        assert (
            int.from_bytes(
                packet[TestSetRawRC.aux4_position : TestSetRawRC.aux4_position + 2],
                "little",
            )
            > 1300
        )
        assert (
            int.from_bytes(
                packet[TestSetRawRC.aux4_position : TestSetRawRC.aux4_position + 2],
                "little",
            )
            < 1700
        )

        assert (
            int.from_bytes(
                packet[
                    TestSetRawRC.throttle_position : TestSetRawRC.throttle_position + 2
                ],
                "little",
            )
            == 1500
        )
