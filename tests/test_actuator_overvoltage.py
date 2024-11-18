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
    SEVERITY_WARNING = 'WARNING'
    MODE_APPEARS = 'APPEARS'
    MODE_DISAPPEARS = 'DISAPPEARS'

    # Define constants for the diagnostic message codes
    ERROR_CODE_OVERVOLTAGE = 20752

    def test_ua_overvoltage(self):
        """
        Testet das Verhalten des Aktorausgangs bei Überspannung 
        und prüft die korrekten Warn- und Entwarnungsereignisse.
        
        
        return: None

        """

        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)
        tc.set_output_active(True)
        time.sleep(2)

        tc.set_actuator_voltage(self._over_voltage)
        time.sleep(2)
        overvoltage_diag = dut.get_event()

        tc.set_actuator_voltage(self._nominal_voltage)
        time.sleep(2)
        normal_diag = dut.get_event()


        self.assertEqual(self.SEVERITY_WARNING, overvoltage_diag[0]['severity'])
        self.assertEqual(self.ERROR_CODE_OVERVOLTAGE, overvoltage_diag[0]['message']['code'])
        self.assertEqual(self.MODE_APPEARS, overvoltage_diag[0]['message']['mode'])
        self.assertEqual(master, overvoltage_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, overvoltage_diag[0]['origin']['portNumber'])

        self.assertEqual(self.SEVERITY_WARNING, normal_diag[0]['severity'])
        self.assertEqual(self.ERROR_CODE_OVERVOLTAGE, normal_diag[0]['message']['code'])
        self.assertEqual(self.MODE_DISAPPEARS, normal_diag[0]['message']['mode'])
        self.assertEqual(master, normal_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, normal_diag[0]['origin']['portNumber'])

        tc.set_output_active(False)

if __name__ == '__main__':
    unittest.main()

