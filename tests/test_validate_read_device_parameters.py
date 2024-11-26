import unittest
import time
from library.testsystemdevice.TestConfigurations import *

class Parameter(unittest.TestCase):


    # Define constans for voltage levels
    _nominal_voltage = 24.0
    _no_voltage = 10.0
    _under_voltage = 16.0
    _over_voltage = 32.0
    _port = port

    # Define parameters
    VENDOR_NAME = 16
    VENDOR_TEXT = 17
    PRODUCT_NAME = 18
    PRODUCT_ID = 19
    PRODUCT_TEXT = 20
    HARDWARE_REVISION = 22
    SOFTWARE_REVISION = 23   
    DEVICE_TAG = 36

    # Define paramter values
    VENDOR_NAME_VALUE = [77, 117, 114, 114, 101, 108, 101, 107, 116, 114, 111, 110, 105, 107, 32, 71, 109, 98, 72]
    VENDOR_TEXT_VALUE = [77, 117, 114, 114, 101, 108, 101, 107, 116, 114, 111, 110, 105, 107, 32, 45, 32, 115, 116, 97, 121, 32, 99, 111, 110, 110, 101, 99, 116, 101, 100]
    PRODUCT_NAME_VALUE = [77, 86, 80, 49, 50, 78, 45, 80, 54, 32, 68, 73, 79, 49, 54, 65, 32, 56, 120, 77, 49, 50, 32, 73, 79, 76, 65, 49, 50, 32, 66, 48]
    PRODUCT_ID_VALUE = [53, 57, 50, 49, 57]
    PRODUCT_TEXT_VALUE = [68, 105, 103, 105, 116, 97, 108, 32, 72, 117, 98]
    HARDWARE_REVISION_VALUE = [86, 45, 49, 46, 48, 48, 46, 48, 48]
    SOFTWARE_REVISION_VALUE = [80, 46, 48, 46, 48, 48, 46, 48, 51] 
    DEVICE_TAG_VALUE = [0]

    def test_read_parameter(self):
        """
        Liest die Parameter des Geräts aus und prüft ihre Gültigkeit.
        
        
        return: None
        """

        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)
        tc.set_output_active(True)
        time.sleep(2)

        self.assertEqual(self.VENDOR_NAME_VALUE, dut.get_parameters(self.VENDOR_NAME))
        self.assertEqual(self.VENDOR_TEXT_VALUE, dut.get_parameters(self.VENDOR_TEXT))
        self.assertEqual(self.PRODUCT_NAME_VALUE, dut.get_parameters(self.PRODUCT_NAME))
        self.assertEqual(self.PRODUCT_ID_VALUE, dut.get_parameters(self.PRODUCT_ID))
        self.assertEqual(self.PRODUCT_TEXT_VALUE, dut.get_parameters(self.PRODUCT_TEXT))
        self.assertEqual(self.HARDWARE_REVISION_VALUE, dut.get_parameters(self.HARDWARE_REVISION))
        self.assertEqual(self.SOFTWARE_REVISION_VALUE, dut.get_parameters(self.SOFTWARE_REVISION))
        self.assertEqual(self.DEVICE_TAG_VALUE, dut.get_parameters(self.DEVICE_TAG))

        tc.set_output_active(False)

if __name__ == '__main__':
    unittest.main()

