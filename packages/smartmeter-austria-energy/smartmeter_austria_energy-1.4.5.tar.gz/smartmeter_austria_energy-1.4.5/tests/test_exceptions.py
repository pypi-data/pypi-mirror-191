"""Tests the exception classes."""

from src.smartmeter_austria_energy.exceptions import (
    SmartmeterException,
    SmartmeterSerialException,
    SmartmeterTimeoutException,
)


def test_SmartmeterException_Is_Exception():
    """Test the SmartmeterException class."""
    # arrange

    # act
    my_exception = SmartmeterException()

    # assert
    assert isinstance(my_exception, Exception)


def test_SmartmeterTimeoutException_Is_Exception():
    """Test the SmartmeterTimeoutException class."""
    # arrange

    # act
    my_exception = SmartmeterTimeoutException()

    # assert
    assert isinstance(my_exception, SmartmeterException)


def test_SmartmeterSerialException_Is_Exception():
    """Test the SmartmeterSerialException class."""
    # arrange

    # act
    my_exception = SmartmeterSerialException()

    # assert
    assert isinstance(my_exception, SmartmeterException)
    assert isinstance(my_exception, Exception)
