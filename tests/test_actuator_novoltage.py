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

    # Define constants for severity levels and modes
    SEVERITY_ERROR = 'ERROR'
    MODE_APPEARS = 'APPEARS'
    MODE_DISAPPEARS = 'DISAPPEARS'

    # Define constants for the diagnostic message codes
    ERROR_CODE_NOVOLTAGE = 20736

    def test_ua_novoltage(self):
        """
        Testet das Verhalten des Aktorausgangs bei keiner Spannung 
        und prüft die korrekten Warn- und Entwarnungsereignisse.
        
        
        return: None
        """

        tc = get_testcube()
        dut = tc.dut()

        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)
        tc.set_output_active(True)
        time.sleep(2)


        tc.set_actuator_voltage(self._no_voltage)
        time.sleep(2)
        diags_novoltage = dut.get_event()

        tc.set_actuator_voltage(self._nominal_voltage)
        time.sleep(2)
        normal_diag = dut.get_event()


        self.assertEqual(self.SEVERITY_ERROR, diags_novoltage[0]['severity'])
        self.assertEqual(self.ERROR_CODE_NOVOLTAGE, diags_novoltage[0]['message']['code'])
        self.assertEqual(self.MODE_APPEARS, diags_novoltage[0]['message']['mode'])
        self.assertEqual(master, diags_novoltage[0]['origin']['masterNumber'])
        self.assertEqual(self._port, diags_novoltage[0]['origin']['portNumber'])

        self.assertEqual(self.SEVERITY_ERROR, normal_diag[0]['severity'])
        self.assertEqual(self.ERROR_CODE_NOVOLTAGE, normal_diag[0]['message']['code'])
        self.assertEqual(self.MODE_DISAPPEARS, normal_diag[0]['message']['mode'])
        self.assertEqual(master, normal_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, normal_diag[0]['origin']['portNumber'])

        tc.set_output_active(False)

if __name__ == '__main__':
    unittest.main()

