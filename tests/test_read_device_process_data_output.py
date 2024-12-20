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
    PROCESS_DATA_OUTPUT = 41

    def process_data_output(self):
        """
        Gibt ProcessDataOutput aus.
        
        
        return: ProcessDataOutput
        """

        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)
        tc.set_output_active(True)
        time.sleep(2)
        
        print("ProcessDataOutput: " + dut.get_parameters(self.PROCESS_DATA_OUTPUT))

        tc.set_output_active(False)
        
if __name__ == '__main__':
    unittest.main()

