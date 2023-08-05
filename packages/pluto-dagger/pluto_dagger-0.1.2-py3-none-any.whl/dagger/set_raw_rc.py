"""Controls the pluto using RC params"""
from dagger.utils import get_header_bytes, get_direction_in_bytes, calculate_crc
import time


class SetRawRC:
    """Controls the pluto using RC params.

    Parameters
    ----------
    connection : PlutoConnection
        Pluto connection object for communicating with ``Pluto``.

    Examples
    --------
    >>> t = dagger.PlutoConnection()
    >>> t.connect(('Pluto_IP', Pluto_port))
    >>> rc = dagger.SetRawRC(t)
    """
    __msg_length = 16
    __msg_code = 200

    def __init__(self, connection):
        self._connection = connection
        self.roll = 1500  # Roll command = 0
        self.pitch = 1500  # Pitch command = 0
        self.throttle = 1000  # Roll command = 0
        self.yaw = 1500  # Yaw command = 0
        self.aux1 = 1500  # Headfree Mode
        self.aux2 = 1500  # Developer Mode Off
        self.aux3 = 1500  # Altitude Hold Mode
        self.aux4 = 1000  # DISARM Mode

    def set_roll(self, roll):
        """Sets the roll values in pluto

        Parameters
        ----------
        roll : int [900,2100]
            Roll values for Pluto, Roll stick is 0 at 1500 value

        Examples
        --------
        >>> rc.set_roll(roll)
        """
        self.roll = roll
        self._send()

    def set_pitch(self, pitch):
        """Sets the pitch values in pluto

        Parameters
        ----------
        pitch : int [900,2100]
            Pitch values for Pluto, Pitch stick is 0 at 1500 value

        Examples
        --------
        >>> rc.set_pitch(pitch)
        """
        self.pitch = pitch
        self._send()

    def set_throttle(self, throttle):
        """Sets the throttle values in pluto

        Parameters
        ----------
        throttle : int [900,2100]
            Throttle values for Pluto, Throttle stick is 0 at 1500 value

        Examples
        --------
        >>> rc.set_throttle(throttle)
        """
        self.throttle = throttle
        self._send()
    
    def set_rc_roll_pitch(self, roll, pitch):
        self.roll = roll
        self.pitch = pitch
        self._send()
        
    def set_rct(self, roll, pitch, throttle):
        self.roll = roll
        self.pitch = pitch
        self.throttle = throttle
        self._send()

    def set_yaw(self, yaw):
        """Sets the yaw values in pluto

        Parameters
        ----------
        yaw : int [900,2100]
            Yaw values for Pluto, Yaw stick is 0 at 1500 value

        Examples
        --------
        >>> rc.set(yaw)
        """
        self.yaw = yaw
        self._send()

    def set_maghold_mode(self):
        """Sets the Mag Hold Mode in pluto

        Examples
        --------
        >>> rc.set_maghold_mode()
        """
        self.aux1 = 1100
        self._send()

    def set_headfree_mode(self):
        """Sets the Headfree mode in pluto

        Examples
        --------
        >>> rc.set_headfree_mode()
        """
        self.aux1 = 1500
        self._send()

    def set_developer_mode_off(self):
        """Disables the Developer mode in pluto

        Examples
        --------
        >>> rc.set_developer_mode_off()
        """
        self.aux2 = 1500
        self._send()

    def set_developer_mode_on(self):
        """Enables the Developer mode in pluto

        Examples
        --------
        >>> rc.set_developer_mode_on()
        """
        self.aux2 = 1100
        self._send()

    def set_alt_hold_mode(self):
        """Enables the Alt Hold mode in pluto

        Examples
        --------
        >>> rc.set_alt_hold_mode()
        """
        self.aux3 = 1500
        self._send()

    def set_throttle_free_mode(self):
        """Enables the Throttle free mode in pluto

        Examples
        --------
        >>> rc.set_throttle_free_mode()
        """
        self.aux3 = 1100
        self._send()

    def arm_drone(self):
        """Arms the drone

        Examples
        --------
        >>> rc.arm_drone()
        """
        self.aux4 = 1500
        self.throttle = 1000
        self._send()

    def box_arm(self):
        """Box-arms the drone

        Examples
        --------
        >>> rc.box_arm()
        """
        self.roll = 1500  # Roll command = 0
        self.pitch = 1500  # Pitch command = 0
        self.throttle = 1500  # Roll command = 0
        self.yaw = 1500  # Yaw command = 0
        self.aux4 = 1500
        self._send()
        print("box arming")
        time.sleep(0.5)

    def disarm_drone(self):
        """Disarms the drone

        Examples
        --------
        >>> rc.disarm_drone()
        """
        self.aux4 = 1200
        self.throttle = 1300
        self._send()
        print("disarming")
        time.sleep(0.5)

    def _send(self):
        """Sends the RC Packet"""
        header = get_header_bytes()
        direction = get_direction_in_bytes()

        length_bytes = bytearray(SetRawRC.__msg_length.to_bytes(1, byteorder="little"))
        code_bytes = bytearray(SetRawRC.__msg_code.to_bytes(1, byteorder="little"))

        roll_bytes = bytearray(self.roll.to_bytes(2, byteorder="little"))
        pitch_bytes = bytearray(self.pitch.to_bytes(2, byteorder="little"))
        throttle_bytes = bytearray(self.throttle.to_bytes(2, byteorder="little"))
        yaw_bytes = bytearray(self.yaw.to_bytes(2, byteorder="little"))

        aux1_bytes = bytearray(self.aux1.to_bytes(2, byteorder="little"))
        aux2_bytes = bytearray(self.aux2.to_bytes(2, byteorder="little"))
        aux3_bytes = bytearray(self.aux3.to_bytes(2, byteorder="little"))
        aux4_bytes = bytearray(self.aux4.to_bytes(2, byteorder="little"))

        payload = (roll_bytes + pitch_bytes + throttle_bytes + yaw_bytes + aux1_bytes +
                   aux2_bytes + aux3_bytes + aux4_bytes)

        message = length_bytes + code_bytes + payload
        crc = calculate_crc(message)
        packet = header + direction + message
        packet.append(crc)
        self._connection.send(packet)
