import unittest
import time
from testsystemdevice.test_configurations import *

class UsUaDiags(unittest.TestCase):
    _nominal_voltage = 24.0
    _no_voltage = 10.0
    _under_voltage = 16.0
    _over_voltage = 32.0
    _port = port+1

    def test_us_undervoltage(self):

        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)
        time.sleep(1)

        tc.set_sensor_voltage(self._under_voltage)
        time.sleep(1)
        undervoltage_diag = dut.get_event()

        tc.set_sensor_voltage(self._nominal_voltage)
        time.sleep(2)

        
        normal_diag = dut.get_event()

        self.assertEqual('WARNING', undervoltage_diag[0]['severity'])
        self.assertEqual(20753, undervoltage_diag[0]['message']['code'])
        self.assertEqual('APPEARS', undervoltage_diag[0]['message']['mode'])
        self.assertEqual(master, undervoltage_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, undervoltage_diag[0]['origin']['portNumber'])

        self.assertEqual('WARNING', normal_diag[0]['severity'])
        self.assertEqual(20753, normal_diag[0]['message']['code'])
        self.assertEqual('DISAPPEARS', normal_diag[0]['message']['mode'])
        self.assertEqual(master, normal_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, normal_diag[0]['origin']['portNumber'])


    def test_us_overvoltage(self):
        
        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)
        time.sleep(1)

        tc.set_sensor_voltage(self._over_voltage)
        time.sleep(1)
        overvoltage_diag = dut.get_event()

        tc.set_sensor_voltage(self._nominal_voltage)
        time.sleep(2)

        normal_diag = dut.get_event()

        self.assertEqual('WARNING', overvoltage_diag[0]['severity'])
        self.assertEqual(20752, overvoltage_diag[0]['message']['code'])
        self.assertEqual('APPEARS', overvoltage_diag[0]['message']['mode'])
        self.assertEqual(master, overvoltage_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, overvoltage_diag[0]['origin']['portNumber'])

        self.assertEqual('WARNING', normal_diag[0]['severity'])
        self.assertEqual(20752, normal_diag[0]['message']['code'])
        self.assertEqual('DISAPPEARS', normal_diag[0]['message']['mode'])
        self.assertEqual(master, normal_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, normal_diag[0]['origin']['portNumber']) 


    # def test_ua_novoltage(self):
    #     # Arrange
    #     tc = get_testcube()
    #     dut = tc.dut()

    #     tc.set_sensor_voltage(self._nominal_voltage)
    #     tc.set_actuator_voltage(self._nominal_voltage)

    #     dut.wait_till_reachable(initial_wait_time=0, timeout_sec=60)
    #     self.assertEqual(0, len(dut.get_diagnostics()))

    #     # Action
    #     tc.set_actuator_voltage(self._no_voltage)
    #     time.sleep(5)

    #     diags_novoltage = dut.get_diagnostics()

    #     tc.set_actuator_voltage(self._nominal_voltage)
    #     time.sleep(5)

    #     diags_normal = dut.get_diagnostics()

    #     # Assert
    #     novoltage_diag = diags_novoltage[0]
    #     self.assertEqual(True, novoltage_diag.valid)
    #     self.assertEqual(Severity.Warning, novoltage_diag.severity)
    #     self.assertEqual(Mode.Appears, novoltage_diag.mode)
    #     self.assertEqual(Category.SystemDiagnostic, novoltage_diag.category)
    #     self.assertEqual(0x8000, novoltage_diag.channelNumber)
    #     self.assertEqual(268, novoltage_diag.errorIdentifier)
    #     self.assertEqual([0, 0], novoltage_diag.errorExtension)

    #     self.assertEqual(0, len(diags_normal))

    # def test_ua_undervoltage(self):
    #     # Arrange
    #     tc = get_testcube()
    #     dut = tc.dut()

    #     tc.set_sensor_voltage(self._nominal_voltage)
    #     tc.set_actuator_voltage(self._nominal_voltage)

    #     dut.wait_till_reachable(initial_wait_time=0, timeout_sec=60)
    #     self.assertEqual(0, len(dut.get_diagnostics()))

    #     # Action
    #     tc.set_actuator_voltage(self._under_voltage)
    #     time.sleep(5)

    #     diags_undervoltage = dut.get_diagnostics()

    #     tc.set_actuator_voltage(self._nominal_voltage)
    #     time.sleep(5)

    #     diags_normal = dut.get_diagnostics()

    #     # Assert
    #     undervoltage_diag = diags_undervoltage[0]
    #     self.assertEqual(True, undervoltage_diag.valid)
    #     self.assertEqual(Severity.Warning, undervoltage_diag.severity)
    #     self.assertEqual(Mode.Appears, undervoltage_diag.mode)
    #     self.assertEqual(Category.SystemDiagnostic, undervoltage_diag.category)
    #     self.assertEqual(0x8000, undervoltage_diag.channelNumber)
    #     self.assertEqual(262, undervoltage_diag.errorIdentifier)
    #     self.assertEqual([0, 0], undervoltage_diag.errorExtension)

    #     self.assertEqual(0, len(diags_normal))

    # def test_ua_overvoltage(self):
    #     # Arrange
    #     tc = get_testcube()
    #     dut = tc.dut()

    #     tc.set_sensor_voltage(self._nominal_voltage)
    #     tc.set_actuator_voltage(self._nominal_voltage)

    #     dut.wait_till_reachable(initial_wait_time=0, timeout_sec=60)
    #     self.assertEqual(0, len(dut.get_diagnostics()))

    #     # Action
    #     tc.set_actuator_voltage(self._over_voltage)
    #     time.sleep(5)

    #     diags_overvoltage = dut.get_diagnostics()

    #     tc.set_actuator_voltage(self._nominal_voltage)
    #     time.sleep(5)

    #     diags_normal = dut.get_diagnostics()

    #     # Assert
    #     overvoltage_diag = diags_overvoltage[0]
    #     self.assertEqual(True, overvoltage_diag.valid)
    #     self.assertEqual(Severity.Warning, overvoltage_diag.severity)
    #     self.assertEqual(Mode.Appears, overvoltage_diag.mode)
    #     self.assertEqual(Category.SystemDiagnostic, overvoltage_diag.category)
    #     self.assertEqual(0x8000, overvoltage_diag.channelNumber)
    #     self.assertEqual(263, overvoltage_diag.errorIdentifier)
    #     self.assertEqual([0, 0], overvoltage_diag.errorExtension)

    #     self.assertEqual(0, len(diags_normal))

if __name__ == '__main__':
    unittest.main()
