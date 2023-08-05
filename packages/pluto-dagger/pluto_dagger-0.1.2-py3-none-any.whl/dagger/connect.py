"""Defines API Connection"""
import socket


class PlutoConnection(socket.socket):
    """Handles connection with drone."""

    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
