"""Tests the Smartmeter class."""

import pytest

from src.smartmeter_austria_energy.exceptions import SmartmeterException
from src.smartmeter_austria_energy.smartmeter import Smartmeter
from src.smartmeter_austria_energy.supplier import SUPPLIER_EVN_NAME


def test_smartmeter_constructor():
    """Test the constructor of the smartmeter class with an empty port."""

    # arrange
    supplier_name = SUPPLIER_EVN_NAME
    key_hex_string = "some_hex"
    port = "COM5"

    # act
    my_smartmeter = Smartmeter(supplier_name, port, key_hex_string)

    # assert
    assert isinstance(my_smartmeter, Smartmeter)


@pytest.mark.asyncio
async def test_smartmeter_has_empty_port():
    supplier_name = SUPPLIER_EVN_NAME
    key_hex_string = "some_hex"
    port = ""

    my_smartmeter = Smartmeter(supplier_name, port, key_hex_string)
    with pytest.raises(SmartmeterException):
        my_smartmeter.read()
