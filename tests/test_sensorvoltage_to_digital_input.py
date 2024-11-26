import unittest
import time
from library.testsystemdevice.TestConfigurations import *

class Diags(unittest.TestCase):

    # Define constans for voltage levels
    _nominal_voltage = 24.0
    _no_voltage = 10.0
    _under_voltage = 16.0
    _over_voltage = 32.0
    _port = port

    # Define parameters
    DEVICE_TAG = 36

    def test_us_input(self):

        """
        Testet das Verhalten des Systems, wenn eine Sensorspannung auf einen Eingangspin gesetzt wird.
        Überprüft, ob die richtige Antwort und der korrekte Pinzustand erkannt werden.



        return: None
        """
        
        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)
        tc.set_output_active(True)
        time.sleep(2)
                
        tc.peripheral_configuration().ioldevice_bridge_x2_pin1_to_pin2_and_pin4()
        time.sleep(2)
        input_diag = dut.get_processdata_getdata_value()

        tc.peripheral_configuration().ioldevice_bridge_x2_pin1_to_pin2_and_pin4(False)
        time.sleep(2)
        normal_diag = dut.get_processdata_getdata_value()

        self.assertEqual(16, input_diag['iolink']['value'][0])
        self.assertEqual(0, normal_diag['iolink']['value'][0])
        self.assertEqual([0], dut.get_parameters(self.DEVICE_TAG))

        tc.set_output_active(False)

if __name__ == '__main__':
    unittest.main()

