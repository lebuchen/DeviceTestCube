import unittest
import time
from library.testsystemdevice.test_configurations import *

class Diags(unittest.TestCase):

    # Define constans for voltage levels
    _nominal_voltage = 24.0
    _no_voltage = 10.0
    _under_voltage = 16.0
    _over_voltage = 32.0
    _port = port

    # Define Parameters
    DEVICE_TAG = 36

    def test_input_output(self):
            
        """
        Testet Überprüft das Verhalten des Systems, wenn ein Ausgang mit einem Eingangspin verbunden wird.
        Überprüft ob die korrekte Antwort geliefert und der Pinzustand richtig erkannt wird.
        
        
        return: None
        """

        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)
        tc.set_output_active(True)
        time.sleep(2)

        dut.post_processdata_value(True, None , [0, 3] , True)
        time.sleep(2)
        input_diag = dut.get_processdata_getdata_value()


        dut.post_processdata_value(False, None , [0, 0] , False)
        time.sleep(2)
        normal_diag = dut.get_processdata_getdata_value()

        self.assertEqual(3, input_diag['iolink']['value'][0])
        self.assertEqual(3, input_diag['iolink']['value'][1])

        self.assertEqual(0, normal_diag['iolink']['value'][0])
        self.assertEqual(0, normal_diag['iolink']['value'][1])

        self.assertEqual([0], dut.get_parameters(self.DEVICE_TAG))

        tc.set_output_active(False)

if __name__ == '__main__':
    unittest.main()

