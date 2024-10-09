import unittest
import time
from testsystemdevice.test_configurations import get_testcube

class UsUaDiags(unittest.TestCase):
    _nominal_voltage = 24.0
    _no_voltage = 10.0
    _under_voltage = 16.0
    _over_voltage = 32.0

    def test_us_undervoltage(self):
        # Arrange
        tc = get_testcube()
        dut = tc.dut()

        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)

        # dut.wait_till_reachable(initial_wait_time=0, timeout_sec=60)
        # self.assertEqual(0, len(dut.get_diagnostics()))

        tc.set_sensor_voltage(self._under_voltage)
        time.sleep(5)

        undervoltage_diag = dut.get_event()

        tc.set_sensor_voltage(self._nominal_voltage)
        time.sleep(5)

        diags_normal = dut.get_event()

        self.assertEqual('ERROR', undervoltage_diag['severity'])
        self.assertEqual(6144, undervoltage_diag['message']['code'])
        self.assertEqual('APPEARS', undervoltage_diag['message']['mode'])
        self.assertEqual(1, undervoltage_diag['origin']['masterNumber'])
        self.assertEqual(1, undervoltage_diag['origin']['portNumber'])

        self.assertEqual('ERROR', diags_normal['severity'])
        self.assertEqual(6144, diags_normal['message']['code'])
        self.assertEqual('DISAPPEARS', diags_normal['message']['mode'])
        self.assertEqual(1, diags_normal['origin']['masterNumber'])
        self.assertEqual(1, diags_normal['origin']['portNumber'])


    # def test_us_overvoltage(self):
    #     # Arrange
    #     tc = get_testcube()
    #     dut = tc.dut()

    #     tc.set_sensor_voltage(self._nominal_voltage)
    #     tc.set_actuator_voltage(self._nominal_voltage)

    #     dut.wait_till_reachable(initial_wait_time=0, timeout_sec=60)
    #     self.assertEqual(0, len(dut.get_diagnostics()))

    #     # Action
    #     tc.set_sensor_voltage(self._over_voltage)
    #     time.sleep(5)

    #     diags_overvoltage = dut.get_diagnostics()

    #     tc.set_sensor_voltage(self._nominal_voltage)
    #     time.sleep(5)

    #     diags_normal = dut.get_diagnostics()

    #     # Assert
    #     overvoltage_diag = diags_overvoltage[0]
    #     self.assertEqual(True, overvoltage_diag.valid)
    #     self.assertEqual(Severity.Warning, overvoltage_diag.severity)
    #     self.assertEqual(Mode.Appears, overvoltage_diag.mode)
    #     self.assertEqual(Category.SystemDiagnostic, overvoltage_diag.category)
    #     self.assertEqual(0x8000, overvoltage_diag.channelNumber)
    #     self.assertEqual(257, overvoltage_diag.errorIdentifier)
    #     self.assertEqual([0, 0], overvoltage_diag.errorExtension)

    #     self.assertEqual(0, len(diags_normal))

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
