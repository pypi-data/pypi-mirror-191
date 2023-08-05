"""Calibrates the accelerometer"""
from dagger.utils import get_header_bytes, get_direction_in_bytes, calculate_crc


class AccCalibration:
    """Calibrates the accelerometer.

    Parameters
    ----------
    connection : PlutoConnection
        Pluto connection object for communicating with ``Pluto``.

    Examples
    --------
    >>> t = dagger.PlutoConnection()
    >>> t.connect(('Pluto_IP', Pluto_port))
    >>> acc_cal = dagger.AccCalibration(t)

    """
    __msg_length = 0
    __msg_code = 205

    def __init__(self, connection):
        self._connection = connection
        self.cmd = 0

    def acc_calibartion(self):
        """Sends the request to calibrate the accelerometer.

        Examples
        --------
        >>> acc_cal.acc_calibration()

        Note
        ----
        Place the drone on a flat surface before starting.
        """
        header = get_header_bytes()
        direction = get_direction_in_bytes()
        length_bytes = bytearray(
            AccCalibration.__msg_length.to_bytes(1, byteorder="little"))
        code_bytes = bytearray(AccCalibration.__msg_code.to_bytes(1, byteorder="little"))

        message = length_bytes + code_bytes
        crc = calculate_crc(message)
        packet = header + direction + message
        packet.append(crc)
        self._connection.send(packet)
