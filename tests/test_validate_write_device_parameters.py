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
    APPLICATION_TAG = 24
    FUNCTION_TAG = 25
    LOCATION_TAG = 26
    DEVICE_TAG = 36

    IDENTIFICATION_ID = 96
    SERIAL_NUMBER = 97


    # Define paramter values
    TEST_VALUE = [116, 101, 115, 116, 10]
    DEVICE_TAG_VALUE = [0]

    def test_write_parameter(self):
        """
        Setzt die Parameter des Geräts, ließt sie aus und prüft ihre Gültigkeit.
        
        
        return: None
        """

        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)
        tc.set_output_active(True)
        time.sleep(2)

        dut.post_parameters(self.TEST_VALUE, self.APPLICATION_TAG)
        dut.post_parameters(self.TEST_VALUE, self.FUNCTION_TAG)
        dut.post_parameters(self.TEST_VALUE, self.LOCATION_TAG)
        self.assertEqual(self.DEVICE_TAG_VALUE, dut.get_parameters(self.DEVICE_TAG))

        # ISDU-Parameter
        dut.post_parameters(self.TEST_VALUE, self.IDENTIFICATION_ID)
        dut.post_parameters(self.TEST_VALUE, self.SERIAL_NUMBER)


        tc.set_sensor_voltage(self._no_voltage)
        tc.set_actuator_voltage(self._no_voltage)
        time.sleep(2)

        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)
        time.sleep(2)


        self.assertEqual(self.TEST_VALUE, dut.get_parameters(self.APPLICATION_TAG))
        self.assertEqual(self.TEST_VALUE, dut.get_parameters(self.FUNCTION_TAG))
        self.assertEqual(self.TEST_VALUE, dut.get_parameters(self.LOCATION_TAG))
        self.assertEqual(self.DEVICE_TAG_VALUE, dut.get_parameters(self.DEVICE_TAG))

        # ISDU-Parameter
        self.assertEqual(self.TEST_VALUE, dut.get_parameters(self.IDENTIFICATION_ID))
        self.assertEqual(self.TEST_VALUE, dut.get_parameters(self.SERIAL_NUMBER))

        tc.set_output_active(False)
        
if __name__ == '__main__':
    unittest.main()

