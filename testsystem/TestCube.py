from mvkpro import MvkPro
from powersupply import PowerSupply
from .PeripheralConfiguration import PeripheralConfiguration

class TestCube:

    def __init__(self) -> None:
        self._dut = None
        self._powersupply = None
        self._channel_us = None
        self._channel_ua = None
        self._relaiscard = None

    def set_dut(self, dut: MvkPro) -> None:
        self._dut = dut

    def set_powersupply(self, powersupply: PowerSupply) -> None:
        self._powersupply = powersupply

    def set_power_supply_channel_us(self, channel: int) -> None:
        self._channel_us = channel

    def set_power_supply_channel_ua(self, channel: int) -> None:
        self._channel_ua = channel

    def set_peripheral_configuration(self, peripheral_configuration: PeripheralConfiguration) -> None:
        self._peripheral_configuration = peripheral_configuration

    def dut(self) -> MvkPro:
        return self._dut

    def powersupply(self) -> PowerSupply:
        return self._powersupply
    
    def peripheral_configuration(self) -> PeripheralConfiguration:
        return self._peripheral_configuration

    def set_actuator_voltage(self, voltage: float) -> None:
        self._powersupply.set_voltage(voltage, self._channel_ua)

    def set_sensor_voltage(self, voltage: float) -> None:
        self._powersupply.set_voltage(voltage, self._channel_us)
