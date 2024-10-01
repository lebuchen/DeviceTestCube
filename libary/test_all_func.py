import unittest
from device.DeviceComm import devicecomm
from testsystemdevice.test_configurations import *


class UsUaDiags(unittest.TestCase):
    _nominal_voltage = 24.0
    _no_voltage = 10.0
    _under_voltage = 16.0
    _over_voltage = 32.0

    def test_us_nodervoltage(self):
        tc = get_testcube()
        dut = tc.dut()
        print(dut.get_event())