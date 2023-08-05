"""Controls for the Pluto Drone."""
from dagger.set_command import SetCommand
from dagger.set_raw_rc import SetRawRC
from dagger.set_command import CmdType


class PlutoControl():
    """Controls for the Pluto Drone.

    Parameters
    ----------
    connection : PlutoConnection
        Pluto connection object for communicating with ``Pluto``.

    Examples
    --------
    >>> t = dagger.PlutoConnection()
    >>> t.connect(('Pluto_IP', Pluto_port))
    >>> control = dagger.PlutoControl(t)
    """

    def __init__(self, connection):
        """Defines the class variable."""
        self.rc = SetRawRC(connection)
        self.com = SetCommand(connection)
        self.connection = connection

    def take_off(self):
        """Take off command for Pluto.

        Examples
        --------
        >>> control.take_off()
        """
        self.rc.disarm_drone()
        self.rc.box_arm()
        self.com.command(CmdType.TAKE_OFF)

    def land(self):
        """Landing command for Pluto.

        Examples
        --------
        >>> control.land()
        """

        self.com.command(CmdType.LAND)

    def pitch_forward(self):
        """Forward Pitch command for Pluto.

        Examples
        --------
        >>> control.pitch_forward()
        """
        self.rc.set_pitch(1600)

    def pitch_backward(self):
        """Backward Pitch command for Pluto.

        Examples
        --------
        >>> control.pitch_backward()
        """
        self.set_pitch(1400)

    def roll_left(self):
        """Left Roll command for Pluto.

        Examples
        --------
        >>> control.roll_left()
        """
        self.rc.set_roll(1400)

    def roll_right(self):
        """Right Roll command for Pluto.

        Examples
        --------
        >>> control.roll_right()
        """
        self.rc.set_roll(1600)

    def left_yaw(self):
        """Left Yaw command for Pluto.

        Examples
        --------
        >>> control.left_yaw()
        """
        self.rc.set_yaw(1200)

    def right_yaw(self):
        """Right Yaw command for Pluto.

        Examples
        --------
        >>> control.right_yaw()
        """
        self.rc.set_yaw(1800)
