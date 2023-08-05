"""Get the RawIMU data from Pluto."""
import struct
from dagger.utils import get_header_bytes, get_direction_in_bytes, calculate_crc, ZERO


class RawIMUData:
    """Formats the RawIMU values.

    Attributes
    ----------
    acc_x : int
        x-values of Pluto accelerometer.
    acc_y : int
        y-values of Pluto accelerometer.
    acc_z : int
        z-values of Pluto accelerometer.
    gyro_x : int
        x-values of Pluto gyroscope.
    gyro_y : int
        y-values of Pluto gyroscope.
    gyro_z : int
        z-values of Pluto gyroscope.
    mag_x : int
        x-values of Pluto magnetometer.
    mag_y : int
        y-values of Pluto magnetometer.
    mag_z : int
        z-values of Pluto magnetometer.
    timstamp : float
        timestamp values of pluto in the ``seconds`` Units.
    Example
    -------
    >>> RawIMUdata.acc_x
    """

    def __init(self, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z):
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.acc_z = acc_z
        self.gyro_x = gyro_x
        self.gyro_y = gyro_y
        self.gyro_z = gyro_z
        self.mag_x = mag_x
        self.mag_y = mag_y
        self.mag_z = mag_z


class RawIMU:
    """Get the RawIMU data from Pluto.

    Parameters
    ----------
    connection : PlutoConnection
        Pluto connection object for communicating with ``Pluto``.

    Examples
    --------
    >>> t = dagger.PlutoConnection()
    >>> t.connect(('Pluto_IP', Pluto_port))
    >>> rawimu = dagger.RawIMU(t)
    """
    __msg_length = 18
    __msg_code = 102

    def __init__(self, connection):
        self._connection = connection

    def get_raw_imu(self):
        """Get the RawIMU OUT package from pluto.

        Returns
        -------
        RawIMUData
            The x,y,z values of accelerometer,gyroscope and magnetometer and the
            timestamp value.

        Examples
        --------
        >>> data = rawimu.get_raw_imu()
        >>> data.acc_x
        """
        header = get_header_bytes()
        direction = get_direction_in_bytes()

        length_bytes = bytearray(ZERO.to_bytes(1, byteorder="little"))
        code_bytes = bytearray(RawIMU.__msg_code.to_bytes(1, byteorder="little"))

        crc = calculate_crc(length_bytes + code_bytes)
        packet = header + direction + length_bytes + code_bytes
        packet.append(crc)
        self._connection.send(packet)

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

                        if size == self.__msg_length and code == self.__msg_code:
                            data = self._connection.recv(6)
                            crc = self._connection.recv(1)
                            temp = struct.unpack("<hhhhhhhhh", data)

                            acc_x = temp[0]
                            acc_y = temp[1]
                            acc_z = temp[2]
                            gyro_x = temp[0]
                            gyro_y = temp[1]
                            gyro_z = temp[2]
                            mag_x = temp[0]
                            mag_y = temp[1]
                            mag_z = temp[2]

                            imu_data = RawIMUData(
                                acc_x,
                                acc_y,
                                acc_z,
                                gyro_x,
                                gyro_y,
                                gyro_z,
                                mag_x,
                                mag_y,
                                mag_z,
                            )
                            return imu_data
