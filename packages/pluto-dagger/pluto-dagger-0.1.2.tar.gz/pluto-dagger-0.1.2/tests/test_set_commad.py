import dagger.set_command as cmd
import unittest
from unittest.mock import Mock


class TestSetCommand(unittest.TestCase):
    msg_length = 2
    msg_code = 217

    def test_command(self):
        connection = Mock()
        command = cmd.SetCommand(connection)
        command.command(cmd.CmdType.TAKE_OFF)
        packet = connection.send.call_args.args[0]

        assert chr(packet[0]) == "$"
        assert chr(packet[1]) == "M"
        assert chr(packet[2]) == "<"
        assert packet[3] == TestSetCommand.msg_length
        assert packet[4] == TestSetCommand.msg_code
        assert int.from_bytes(packet[5:7], "little") == 1

        command.command(cmd.CmdType.LAND)
        packet = connection.send.call_args.args[0]
        assert int.from_bytes(packet[5:7], "little") == 2

        command.command(cmd.CmdType.BACK_FLIP)
        packet = connection.send.call_args.args[0]
        assert int.from_bytes(packet[5:7], "little") == 3

        command.command(cmd.CmdType.FRONT_FLIP)
        packet = connection.send.call_args.args[0]
        assert int.from_bytes(packet[5:7], "little") == 4

        command.command(cmd.CmdType.RIGHT_FLIP)
        packet = connection.send.call_args.args[0]
        assert int.from_bytes(packet[5:7], "little") == 5

        command.command(cmd.CmdType.LEFT_FLIP)
        packet = connection.send.call_args.args[0]
        assert int.from_bytes(packet[5:7], "little") == 6
