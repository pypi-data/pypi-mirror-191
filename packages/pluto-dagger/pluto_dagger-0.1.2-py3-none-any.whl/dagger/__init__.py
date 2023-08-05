"""API defining checkpoint"""
import sys
from dagger.acc_calibration import AccCalibration
from dagger.altitude import Altitude
from dagger.analog import Analog
from dagger.attitude import Attitude
from dagger.connect import PlutoConnection
from dagger.control import PlutoControl
from dagger.sensor import PlutoSensor
from dagger.mag_calibration import MagCalibration
from dagger.raw_imu import RawIMU
from dagger.set_command import SetCommand, CmdType
from dagger.set_raw_rc import SetRawRC

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
