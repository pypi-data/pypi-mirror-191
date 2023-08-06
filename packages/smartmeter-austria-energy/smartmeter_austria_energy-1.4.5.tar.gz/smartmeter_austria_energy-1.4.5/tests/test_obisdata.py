"""OBIS data classes tests."""

from src.smartmeter_austria_energy.constants import PhysicalUnits
from src.smartmeter_austria_energy.decrypt import Decrypt
from src.smartmeter_austria_energy.obisdata import ObisData
from src.smartmeter_austria_energy.obisvalue import ObisValueFloat, ObisValueString
from src.smartmeter_austria_energy.supplier import SupplierTINETZ


def test_ObisData_constructor():
    """Test the obisdata constructor."""

    # arrange

    # act
    obisdata = ObisData(dec=None, wanted_values=[])

    # assert
    assert isinstance(obisdata, ObisData)


def test_ObisData_properties():
    """Test the obisdata constructor."""

    # arrange
    obisdata = ObisData(dec=None, wanted_values=[])

    # act
    current1 = obisdata.CurrentL1
    current2 = obisdata.CurrentL2
    current3 = obisdata.CurrentL3

    voltage1 = obisdata.VoltageL1
    voltage2 = obisdata.VoltageL2
    voltage3 = obisdata.VoltageL3

    realPowerIn = obisdata.RealPowerIn
    realPowerOut = obisdata.RealPowerOut
    realPowerDelta = obisdata.RealPowerDelta

    realEnergyIn = obisdata.RealEnergyIn
    realEnergyOut = obisdata.RealEnergyOut

    reactiveEnergyIn = obisdata.ReactiveEnergyIn
    reactiveEnergyOut = obisdata.ReactiveEnergyOut

    deviceNumber = obisdata.DeviceNumber
    logicalDeviceNumber = obisdata.LogicalDeviceNumber

    # assert
    assert isinstance(current1, ObisValueFloat)
    assert current1.RawValue == 0
    assert current1.Unit == PhysicalUnits.A

    assert isinstance(current2, ObisValueFloat)
    assert current2.RawValue == 0
    assert current2.Unit == PhysicalUnits.A

    assert isinstance(current3, ObisValueFloat)
    assert current3.RawValue == 0
    assert current3.Unit == PhysicalUnits.A

    assert isinstance(voltage1, ObisValueFloat)
    assert voltage1.RawValue == 0
    assert voltage1.Unit == PhysicalUnits.V

    assert isinstance(voltage2, ObisValueFloat)
    assert voltage2.RawValue == 0
    assert voltage2.Unit == PhysicalUnits.V

    assert isinstance(voltage3, ObisValueFloat)
    assert voltage3.RawValue == 0
    assert voltage3.Unit == PhysicalUnits.V

    assert isinstance(realPowerIn, ObisValueFloat)
    assert realPowerIn.RawValue == 0
    assert realPowerIn.Unit == PhysicalUnits.W

    assert isinstance(realPowerOut, ObisValueFloat)
    assert realPowerOut.RawValue == 0
    assert realPowerOut.Unit == PhysicalUnits.W

    assert isinstance(realPowerDelta, ObisValueFloat)
    assert realPowerDelta.RawValue == 0
    assert realPowerDelta.Unit == PhysicalUnits.W

    assert isinstance(realPowerIn, ObisValueFloat)
    assert realPowerIn.RawValue == 0
    assert realPowerIn.Unit == PhysicalUnits.W

    assert isinstance(realPowerOut, ObisValueFloat)
    assert realPowerOut.RawValue == 0
    assert realPowerOut.Unit == PhysicalUnits.W

    assert isinstance(realEnergyIn, ObisValueFloat)
    assert realEnergyIn.RawValue == 0
    assert realEnergyIn.Unit == PhysicalUnits.Wh

    assert isinstance(realEnergyOut, ObisValueFloat)
    assert realEnergyOut.RawValue == 0
    assert realEnergyOut.Unit == PhysicalUnits.Wh

    assert isinstance(reactiveEnergyIn, ObisValueFloat)
    assert reactiveEnergyIn.RawValue == 0
    assert reactiveEnergyIn.Unit == PhysicalUnits.varh

    assert isinstance(reactiveEnergyOut, ObisValueFloat)
    assert reactiveEnergyOut.RawValue == 0
    assert reactiveEnergyOut.Unit == PhysicalUnits.varh

    assert isinstance(deviceNumber, ObisValueString)
    assert deviceNumber.RawValue == ""

    assert isinstance(logicalDeviceNumber, ObisValueString)
    assert logicalDeviceNumber.RawValue == ""


def test_ObisData_property_setter():
    """Test the obisdata constructor."""

    # arrange
    obisdata = ObisData(dec=None, wanted_values=[])

    obisdata.CurrentL1 = ObisValueFloat(1.1, PhysicalUnits.A, 1)
    obisdata.CurrentL2 = ObisValueFloat(0.77, PhysicalUnits.Undef, -2)
    obisdata.CurrentL3 = ObisValueFloat(0.4, PhysicalUnits.A, 0)

    obisdata.VoltageL1 = ObisValueFloat(1.1, PhysicalUnits.V, 0)
    obisdata.VoltageL2 = ObisValueFloat(10, PhysicalUnits.V, 1)
    obisdata.VoltageL3 = ObisValueFloat(0.4, PhysicalUnits.V, 2)

    # act
    current1 = obisdata.CurrentL1
    current2 = obisdata.CurrentL2
    current3 = obisdata.CurrentL3

    voltage1 = obisdata.VoltageL1
    voltage2 = obisdata.VoltageL2
    voltage3 = obisdata.VoltageL3

    realPowerIn = obisdata.RealPowerIn
    realPowerOut = obisdata.RealPowerOut
    realPowerDelta = obisdata.RealPowerDelta

    realEnergyIn = obisdata.RealEnergyIn
    realEnergyOut = obisdata.RealEnergyOut

    reactiveEnergyIn = obisdata.ReactiveEnergyIn
    reactiveEnergyOut = obisdata.ReactiveEnergyOut

    deviceNumber = obisdata.DeviceNumber
    logicalDeviceNumber = obisdata.LogicalDeviceNumber

    # assert
    assert isinstance(current1, ObisValueFloat)
    assert current1.RawValue == 1.1
    assert current1.Value == 11
    assert current1.ValueString == "11.0 A"
    assert current1.Unit == PhysicalUnits.A

    assert isinstance(current2, ObisValueFloat)
    assert current2.RawValue == 0.77
    assert current2.Value == 0.0077
    assert current2.ValueString == "0.0077 Undef"
    assert current2.Unit == PhysicalUnits.Undef

    assert isinstance(current3, ObisValueFloat)
    assert current3.RawValue == 0.4
    assert current3.Value == 0.4
    assert current3.ValueString == "0.4 A"
    assert current3.Unit == PhysicalUnits.A

    assert isinstance(voltage1, ObisValueFloat)
    assert voltage1.RawValue == 1.1
    assert voltage1.Value == 1.1
    assert voltage1.Unit == PhysicalUnits.V

    assert isinstance(voltage2, ObisValueFloat)
    assert voltage2.RawValue == 10
    assert voltage2.Value == 100
    assert voltage2.Unit == PhysicalUnits.V

    assert isinstance(voltage3, ObisValueFloat)
    assert voltage3.RawValue == 0.4
    assert voltage3.Value == 40
    assert voltage3.Unit == PhysicalUnits.V

    assert isinstance(realPowerIn, ObisValueFloat)
    assert realPowerIn.RawValue == 0
    assert realPowerIn.Unit == PhysicalUnits.W

    assert isinstance(realPowerOut, ObisValueFloat)
    assert realPowerOut.RawValue == 0
    assert realPowerOut.Unit == PhysicalUnits.W

    assert isinstance(realPowerDelta, ObisValueFloat)
    assert realPowerDelta.RawValue == 0
    assert realPowerDelta.Unit == PhysicalUnits.W

    assert isinstance(realPowerIn, ObisValueFloat)
    assert realPowerIn.RawValue == 0
    assert realPowerIn.Unit == PhysicalUnits.W

    assert isinstance(realPowerOut, ObisValueFloat)
    assert realPowerOut.RawValue == 0
    assert realPowerOut.Unit == PhysicalUnits.W

    assert isinstance(realEnergyIn, ObisValueFloat)
    assert realEnergyIn.RawValue == 0
    assert realEnergyIn.Unit == PhysicalUnits.Wh

    assert isinstance(realEnergyOut, ObisValueFloat)
    assert realEnergyOut.RawValue == 0
    assert realEnergyOut.Unit == PhysicalUnits.Wh

    assert isinstance(reactiveEnergyIn, ObisValueFloat)
    assert reactiveEnergyIn.RawValue == 0
    assert reactiveEnergyIn.Unit == PhysicalUnits.varh

    assert isinstance(reactiveEnergyOut, ObisValueFloat)
    assert reactiveEnergyOut.RawValue == 0
    assert reactiveEnergyOut.Unit == PhysicalUnits.varh

    assert isinstance(deviceNumber, ObisValueString)
    assert deviceNumber.RawValue == ""

    assert isinstance(logicalDeviceNumber, ObisValueString)
    assert logicalDeviceNumber.RawValue == ""


def t_Obisdata_no_wanted_values():
    """Test the ObisObisDataValue class."""
    # arrange
    my_wanted_values: list[str] = []
    my_supplier = SupplierTINETZ()
    frame1 = ""
    frame2 = ""
    my_key_hex_string = ""

    my_decrypt = Decrypt(my_supplier, frame1, frame2, my_key_hex_string)

    # act
    my_obisdata = ObisData(dec=my_decrypt, wanted_values=my_wanted_values)

    # assert
    assert my_obisdata is not None
