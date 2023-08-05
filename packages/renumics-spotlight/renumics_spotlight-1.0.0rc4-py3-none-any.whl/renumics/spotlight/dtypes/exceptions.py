"""
    Exceptions raised in dtype handling
"""


class DataTypeException(Exception):
    """
    Base data type exception.
    """


class InvalidFile(DataTypeException):
    """
    File does not exist or is not readable for the respective data type.
    """
