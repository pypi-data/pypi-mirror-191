"""Get the Analog data from Pluto."""
import struct
import time
from dagger.utils import get_direction_in_bytes, get_header_bytes, calculate_crc, ZERO


class AnalogData:
    """Formats the Battery Voltage, Power Meter, RSSI and Amperage values.

    Attributes
    ----------
    vbat : int
        Battery Voltage values of pluto in the ``1/10 Volts`` Units.
    int_power_meter_sum : int
        Power Meter values of pluto.
    rssi : int
        RSSI values of pluto.
    amperage : int
        Amperage values of pluto.
    timstamp : float
        timestamp values of pluto in the ``seconds`` Units.
    Example
    -------
    >>> AnalogData.vbat
    """

    def __init__(self, vbat, int_power_meter_sum, rssi, amperage):
        """Defines the class variables."""
        self.vbat = vbat
        self.int_power_meter_sum = int_power_meter_sum
        self.rssi = rssi
        self.amperage = amperage
        self.timestamp = time.time()


class Analog:
    """Get the Analog data from Pluto.

    Parameters
    ----------
    connection : PlutoConnection
        Pluto connection object for communicating with ``Pluto``.

    Examples
    --------
    >>> t = dagger.PlutoConnection()
    >>> t.connect(('Pluto_IP', Pluto_port))
    >>> analog = dagger.Analog(t)
    """

    __msg_code = 110
    __msg_length = 7

    def __init__(self, connection):
        """Defines the class variable."""
        self._connection = connection
        self.analog = {}

    def get_analog_data(self):
        """Get the Analog OUT package from pluto.

        Returns
        -------
        AnalogData
            The vbat, int_power_meter_sum, rssi, amperage and timestamp values.

        Examples
        --------
        >>> data = analog.get_analog_data()
        >>> data.vbat
        """
        header = get_header_bytes()
        direction = get_direction_in_bytes()
        length_bytes = bytearray(ZERO.to_bytes(1, byteorder="little"))
        code_bytes = bytearray(Analog.__msg_code.to_bytes(1, byteorder="little"))

        message = length_bytes + code_bytes
        crc = calculate_crc(message)
        packet = header + direction + message
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
                            data = self._connection.recv(size)
                            temp = struct.unpack("<BHHH", data)

                            vbat = float(temp[0])
                            int_power_meter_sum = float(temp[1])
                            rssi = float(temp[2])
                            amperage = float(temp[3])

                            analog_data = AnalogData(vbat, int_power_meter_sum, rssi,
                                                     amperage)
                            return analog_data
