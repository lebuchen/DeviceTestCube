from .PowerSupply import PowerSupply
import serial

class Hcs3202(PowerSupply):
    _BAUDRATE = 9600
    _BYTESIZE = 8
    _PARITY = "N"
    _STOPBITS = 1
    _TIMEOUT = 0.1

    def __init__(self, serial_port: str) -> None:
        self._ser = serial.Serial(
            serial_port,
            baudrate=self._BAUDRATE,
            bytesize=self._BYTESIZE,
            parity=self._PARITY,
            stopbits=self._STOPBITS,
            timeout=self._TIMEOUT
        )
        
    def set_output_active(self, active: bool) -> None:
        self._ser.write(f"SOUT {'ON' if active else 'OFF'}\r".encode())

    def set_voltage(self, voltage: float, channel: int = 0) -> None:
        if channel != 0:
            raise Exception("HCS3202 has only one output channel")
        
        self._ser.write(f"VOLT Voltage{voltage}\r".encode())

    def set_max_current(self, max_current: float, channel: int = 0) -> None:
        if channel != 0:
            raise Exception("HCS3202 has only one output channel")
        
        self._ser.write(f"CURR Current{max_current}\r".encode())
