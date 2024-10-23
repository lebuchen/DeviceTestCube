import unittest
from testsystemdevice.test_configurations import get_testcube
import time

class UsUaDiags:
    def test_us_shortcircuit(self):
        """
        Testet das Verhalten bei Kurzschluss der Sensorseite 
        und prüft die korrekten Warn- und Entwarnungsereignisse.
        
        
        return: None
        """

        nominal_voltage = 24.0
        no_voltage = 10.0
        under_voltage = 16.0
        over_voltage = 32.0

        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(nominal_voltage)
        tc.set_actuator_voltage(nominal_voltage)


        tc.peripheral_configuration().ioldevice_bridge_x1_pin1_to_pin3()
        shortvoltage_diag = dut.get_event()

        tc.peripheral_configuration().ioldevice_bridge_x1_pin1_to_pin3(False)
        normal_diag = dut.get_event()



        print(shortvoltage_diag)
        print(normal_diag)

test = UsUaDiags()

test.test_us_shortcircuit()

# if __name__ == '__main__':
#     unittest.main()

 
