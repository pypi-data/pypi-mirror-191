"""Utils for the Dagger python wrapper for Pluto"""
HEADER = "$M"
DIRECTION_IN = "<"
DIRECTION_OUT = ">"
ZERO = 0


def get_header_bytes():
    """Converts the header to bytes"""
    return bytearray(HEADER, "utf-8")


def get_direction_in_bytes():
    """Converts the in direction arrow to bytes"""
    return bytearray(DIRECTION_IN, "utf-8")


def get_direction_out_bytes():
    """Converts the out direction arrow to bytes"""
    return bytearray(DIRECTION_OUT, "utf-8")


def calculate_crc(byte_array):
    """Calculates the checksum for an array of bytes"""
    crc = 0
    for byte in byte_array:
        crc ^= byte
    return crc


def send_out(con, code):
    """Request for OUT packages
    Parameters
    ----------
    con : PlutoConnection
        Pluto connection object for communicating with ``Pluto``.

    code : int
        MSP packet code for the corresponding out packet.
    """
    header = get_header_bytes()
    direction = get_direction_in_bytes()

    length_bytes = bytearray(ZERO.to_bytes(1, byteorder="little"))
    code_bytes = bytearray(code.to_bytes(1, byteorder="little"))
    message = length_bytes + code_bytes
    crc = calculate_crc(message)
    packet = header + direction + message
    packet.append(crc)
    con.send(packet)
