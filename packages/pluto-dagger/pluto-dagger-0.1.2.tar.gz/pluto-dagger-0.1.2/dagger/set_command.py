"""Sets the command in Pluto"""
import enum
from dagger.utils import get_header_bytes, get_direction_in_bytes, calculate_crc


class CmdType(enum.Enum):
    """Maps the Command types to their corresponding int values"""
    TAKE_OFF = 1
    LAND = 2
    BACK_FLIP = 3
    FRONT_FLIP = 4
    RIGHT_FLIP = 5
    LEFT_FLIP = 6


class SetCommand:
    """Sets the command in Pluto.

    Parameters
    ----------
    connection : PlutoConnection
        Pluto connection object for communicating with ``Pluto``.

    Examples
    --------
    >>> t = dagger.PlutoConnection()
    >>> t.connect(('Pluto_IP', Pluto_port))
    >>> com = dagger.SetCommand(t)
    """

    __msg_length = 2
    __msg_code = 217

    def __init__(self, connection):
        self._connection = connection
        self.cmd = 0

    def command(self, cmd):
        """Sets the Command value in pluto
        
        Parameters
        ----------
        cmd : (TAKE_OFF, LAND, FRONT_FLIP, BACK_FLIP, RIGHT_FLIP, LEFT_FLIP)
            Sets the command type to pluto

        Examples
        --------
        >>> com.command(dagger.CmdType.cmd)
        """

        self.cmd = cmd.value
        print(f"runnning the {cmd}")
        self._send()

    def _send(self):
        """Sends the Command Packet"""
        header = get_header_bytes()
        direction = get_direction_in_bytes()
        length_bytes = bytearray(SetCommand.__msg_length.to_bytes(1, byteorder="little"))
        code_bytes = bytearray(SetCommand.__msg_code.to_bytes(1, byteorder="little"))
        payload = bytearray(self.cmd.to_bytes(2, byteorder="little"))

        message = length_bytes + code_bytes + payload
        crc = calculate_crc(message)
        packet = header + direction + message
        packet.append(crc)
        self._connection.send(packet)
