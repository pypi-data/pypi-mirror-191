"""Lights exceptions"""

class BadCommandException(Exception):
    """Raised when the light has responded to a command with an error code"""

class NotEnoughException(Exception):
    """Raised when not all lights have responded to the message"""
