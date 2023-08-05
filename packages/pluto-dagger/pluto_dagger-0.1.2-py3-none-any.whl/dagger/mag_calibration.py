"""Calibrates the magnetometer"""
from dagger.utils import get_header_bytes, get_direction_in_bytes, calculate_crc


class MagCalibration:
    """Calibrates the magnetometer..

    Parameters
    ----------
    connection : PlutoConnection
        Pluto connection object for communicating with ``Pluto``.

    Examples
    --------
    >>> t = dagger.PlutoConnection()
    >>> t.connect(('Pluto_IP', Pluto_port))
    >>> mag_cal = dagger.MagCalibration(t)

    """

    __msg_length = 0
    __msg_code = 206

    def __init__(self, connection):
        """Defines the class variable."""
        self._connection = connection
        self.cmd = 0

    def mag_calibartion(self):
        """Sends the request to calibrate the magnetometer.

        Examples
        --------
        >>> mag_cal.mag_calibration()

        Note
        ----
        Rotate the drone across all its axis until the process.
        """
        header = get_header_bytes()
        direction = get_direction_in_bytes()
        length_bytes = bytearray(
            MagCalibration.__msg_length.to_bytes(1, byteorder="little"))
        code_bytes = bytearray(MagCalibration.__msg_code.to_bytes(1, byteorder="little"))

        message = length_bytes + code_bytes
        crc = calculate_crc(message)
        packet = header + direction + message
        packet.append(crc)
        self._connection.send(packet)
