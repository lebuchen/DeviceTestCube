from .PowerSupply import PowerSupply
import serial


class Toe8950(PowerSupply):
    _BAUDRATE = 9600

    def __init__(self, serial_port: str) -> None:
        self._ser = serial.Serial(serial_port, baudrate=self._BAUDRATE)
        super().__init__()

    def set_output_active(self, active: bool) -> None:
        command = b"EX 0\n"
        if active:
            command = b"EX 1\n"

        self._ser.write(command)

    def set_voltage(self, voltage: float, channel: int = 0) -> None:
        command = f"SEL {str(channel+1)};V {str(voltage)}\n".encode()
        self._ser.write(command)

    def set_max_current(self, max_current: float, channel: int = 0) -> None:
        command = f"SEL {str(channel+1)};C {str(max_current)}\n".encode()
        self._ser.write(command)
