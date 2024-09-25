from enum import Enum
import serial
import PowerSupply

class Objects(Enum):
    NominalVoltage = 2
    NominalCurrent = 3
    SetValueU = 50
    SetValueI = 51
    PowerSupplyControl = 54


class EaPs2000(PowerSupply):
    _BAUDRATE = 115200
    _VOLTAGE_NOMINAL = 42
    _CURRENT_NOMINAL = 6

    def __init__(self, serial_port: str) -> None:
        with serial.Serial(serial_port, baudrate=self._BAUDRATE, parity=serial.PARITY_ODD) as _:
            pass #Check if Serial Communication is working.
        self._serial_port = serial_port
        super().__init__()

    def _send(self, device_node: int, object_p: Objects, data: bytes):
        with serial.Serial(self._serial_port, baudrate=self._BAUDRATE, parity=serial.PARITY_ODD) as ser:
            length = len(data) - 1
            direction = 1  # PC to PowerSupply
            cast_type = 1  # request
            sending_type = 3  # sending of data

            start_delimiter = length & 0xF
            start_delimiter += (direction & 1) << 4
            start_delimiter += (cast_type & 1) << 5
            start_delimiter += (sending_type & 3) << 6
            start_delimiter = start_delimiter.to_bytes(1, "big")

            telegram = (
                start_delimiter
                + device_node.to_bytes(1, "big")
                + int(object_p.value).to_bytes(1, "big")
                + data
            )
            checksum = 0
            for item in telegram:
                checksum = checksum + int(item)
            telegram = telegram + checksum.to_bytes(2, "big")

            ser.write(telegram)
            data = ser.read(6)

    def _calculate_set_value(
        self, set_value: float, nominal_value: int
    ) -> int:
        return int(25600 * set_value / nominal_value)

    def _set_remote_access(self, active: bool) -> None:
        if active:
            self._send(0, Objects.PowerSupplyControl, b"\x10\x10")
            self._send(1, Objects.PowerSupplyControl, b"\x10\x10")
        else:
            self._send(0, Objects.PowerSupplyControl, b"\x10\x00")
            self._send(1, Objects.PowerSupplyControl, b"\x10\x00")

    def _set_output_active(self, active: bool, channel: int) -> None:
        if active:
            self._send(channel, Objects.PowerSupplyControl, b"\x01\x01")
        else:
            self._send(channel, Objects.PowerSupplyControl, b"\x01\x00")

    def _set_voltage(self, voltage: float, channel: int):
        self._send(
            channel,
            Objects.SetValueU,
            self._calculate_set_value(voltage, self._VOLTAGE_NOMINAL).to_bytes(
                2, "big"
            ),
        )

    def _set_max_current(self, max_current: float, channel: int) -> None:
        self._send(
            channel,
            Objects.SetValueI,
            self._calculate_set_value(max_current, 6).to_bytes(2, "big"),
        )

    def set_output_active(self, active: bool) -> None:
        self._set_remote_access(True)

        self._set_output_active(active, 0)
        self._set_output_active(active, 1)

        self._set_remote_access(False)

    def set_voltage(self, voltage: float, channel: int = 0) -> None:
        self._set_remote_access(True)
        self._set_voltage(voltage, channel)
        self._set_remote_access(False)

    def set_max_current(self, max_current: float, channel: int = 0) -> None:
        self._set_remote_access(True)
        self._set_max_current(max_current, channel)
        self._set_remote_access(False)
