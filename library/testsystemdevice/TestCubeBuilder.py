from library.powersupply.PowerSupply import PowerSupply
from library.device.DeviceComm import devicecomm
from .TestCube import TestCube
from .PeripheralConfiguration import PeripheralConfiguration

class TestCubeBuilder:

    def __init__(self) -> None:
        self._testcube = TestCube()

    def set_powersupply(self, powersupply: PowerSupply):
        self._testcube.set_powersupply(powersupply)
        return self

    def set_dut(self, dut: devicecomm):
        self._testcube.set_dut(dut)
        return self

    def set_us_channel(self, channel: int):
        self._testcube.set_power_supply_channel_us(channel)
        return self

    def set_ua_channel(self, channel: int):
        self._testcube.set_power_supply_channel_ua(channel)
        return self

    def set_peripheral_configuration(self, peripheral_configuration: PeripheralConfiguration):
        self._testcube.set_peripheral_configuration(peripheral_configuration)
        return self

    def get_testcube(self) -> TestCube:
        return self._testcube
