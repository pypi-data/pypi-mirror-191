"""Get the Attitude data from Pluto."""
import struct
import time
from dagger.utils import get_direction_in_bytes, get_header_bytes, calculate_crc, ZERO


class AttitudeData:
    """Formats the roll, pitch and yaw values.

    Attributes
    ----------
    roll : int
        Roll values of pluto in the ``Decidegree`` Units.
    pitch : int
        pitch values of pluto in the ``Decidegree`` Units.
    yaw : int
        yaw values of pluto in the ``Degree`` Units.
    timstamp : float
        timestamp values of pluto in the ``seconds`` Units.
    Example
    -------
    >>> AttitudeData.roll
    """

    def __init__(self, roll, pitch, yaw):
        """Defines the class variable."""
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.timestamp = time.time()


class Attitude:
    """Get the Attitude data from Pluto.

    Parameters
    ----------
    connection : PlutoConnection
        Pluto connection object for communicating with ``Pluto``.

    Examples
    --------
    >>> t = dagger.PlutoConnection()
    >>> t.connect(('Pluto_IP', Pluto_port))
    >>> attitude = dagger.Attitude(t)
    """

    __msg_code = 108
    __msg_length = 6

    def __init__(self, connection):
        """Defines the class variable."""
        self._connection = connection
        self.attitude = {}

    def get_attitude_data(self):
        """Get the Attitude OUT package from pluto.

        Returns
        -------
        AttitudeData
            The roll, pitch, yaw and timestamp values.

        Examples
        --------
        >>> data = attitude.get_attitude_data()
        >>> data.roll
        """
        # sending the request to the pluto.
        header = get_header_bytes()
        direction = get_direction_in_bytes()
        length_bytes = bytearray(ZERO.to_bytes(1, byteorder="little"))
        code_bytes = bytearray(Attitude.__msg_code.to_bytes(1, byteorder="little"))

        message = length_bytes + code_bytes
        crc = calculate_crc(message)
        packet = header + direction + message
        packet.append(crc)
        self._connection.send(packet)

        # recieving the attitude OUT package.
        try:
            data = self.__response()
            return data
        except:
            print("Data not recieved.")

    def __response(self):
        """Recieves the OUT packages."""
        while True:
            header = struct.unpack("c", self._connection.recv(1))[0]
            if header.decode("utf-8") == "$":
                header_m = struct.unpack("c", self._connection.recv(1))[0]

                if header_m.decode("utf-8") == "M":
                    direction = struct.unpack("c", self._connection.recv(1))[0]

                    if direction.decode("utf-8") == ">":
                        size = struct.unpack("B", self._connection.recv(1))[0]
                        code = struct.unpack("B", self._connection.recv(1))[0]

                        if size == 6 and code == 108:
                            data = self._connection.recv(6)
                            temp = struct.unpack("<hhh", data)

                            if temp:
                                roll = temp[0]
                                pitch = temp[1]
                                yaw = temp[2]
                                attitude_data = AttitudeData(roll, pitch, yaw)
                            else:
                                attitude_data = AttitudeData(None, None, None)
                            return attitude_data
