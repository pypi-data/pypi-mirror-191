==================
Working Principles
==================

Sockets
=======

We connected to Pluto first by connecting our device to the drone's hotspot, then we used TCP sockets to connect
to the drone using IPV4 scheme and ``socket`` library in python to do the same. The server iss hosted at ``192.168.4.1:23``
We sent the MSP Packet data encoded as bytes to pluto using sockets, the details about the packet is explained below. 

MSP Packets
===========

We used `MSP Packet scheme <http://www.multiwii.com/wiki/index.php?title=Multiwii_Serial_Protocol&oldid=680>`_ to communicate with Pluto, ie send commands, request data and calibrate the drone.
The data of the packet was first encoded into bytes and then sent as a byte stream (array of bytes) to the drone.
The basic structure of the packet has been explained below.

Structure of the Packet
-----------------------

+--------+-----------+----------------+-----------------+--------------+----------+
| Header | Direction | Message Length | Type of Payload | Message Data | Checksum |
+========+===========+================+=================+==============+==========+
| 2 Bytes|  1 Byte   |    1 Byte      |     1 Byte      |   N Bytes    |  1 Byte  |
+--------+-----------+----------------+-----------------+--------------+----------+

Details of the Packet
---------------------

+-----------------+------------+---------------------------------------------------------------------+
| Type of Byte    | ASCII      | Hexadecimal                                                         |
+=================+============+=====================================================================+
| Header          | $M         | 0x24 0x4d                                                           |
+-----------------+------------+---------------------------------------------------------------------+
| Direction       | '<' or '>' | 0x3c (to the drone) or 0x3e (from the drone)                        |
+-----------------+------------+---------------------------------------------------------------------+
| Message Length  |            | 0x00 - 0xff                                                         |
+-----------------+------------+---------------------------------------------------------------------+
| Type of Payload |            | 0x01 - 0xff                                                         |
+-----------------+------------+---------------------------------------------------------------------+
| Payload         |            | Message Body encoded into N bytes                                   |
+-----------------+------------+---------------------------------------------------------------------+
| Checksum        |            | XOR of Bytes of  “Msg length”, “Command” and all bytes of “Payload” |
+-----------------+------------+---------------------------------------------------------------------+

.. image:: ../asset/chart.png
  :alt: Pluto Packet Direction Chart