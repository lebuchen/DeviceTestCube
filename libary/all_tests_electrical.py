import unittest
import time
from testsystemdevice.test_configurations import *

class UsUaDiags(unittest.TestCase):
    """
    Elektronische Test auf Sensor und Aktor -Seite
    
    
    return: Testergebnisse
    """

    _nominal_voltage = 24.0
    _no_voltage = 10.0
    _under_voltage = 16.0
    _over_voltage = 32.0
    _port = port

    def test_us_undervoltage(self):
        """
        Testet das Verhalten des Sensorausgangs bei Unterspannung 
        und prüft die korrekten Warn- und Entwarnungsereignisse.
        
        
        return: None
        """

        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)
        
        time.sleep(5)  #Statt Timer Statusabfrage 

        tc.set_sensor_voltage(self._under_voltage)
        time.sleep(2)
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
        """
        Testet das Verhalten des Sensorausgangs bei Überspannung 
        und prüft die korrekten Warn- und Entwarnungsereignisse.
        
        
        return: None
        """

        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)
       

        tc.set_sensor_voltage(self._over_voltage)
        time.sleep(2)
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


        tc.set_actuator_voltage(self._no_voltage)
        time.sleep(2)
        diags_novoltage = dut.get_event()

        tc.set_actuator_voltage(self._nominal_voltage)
        time.sleep(2)
        normal_diag = dut.get_event()


        self.assertEqual('WARNING', diags_novoltage[0]['severity'])
        self.assertEqual(20752, diags_novoltage[0]['message']['code']) ###########
        self.assertEqual('APPEARS', diags_novoltage[0]['message']['mode'])
        self.assertEqual(master, diags_novoltage[0]['origin']['masterNumber'])
        self.assertEqual(self._port, diags_novoltage[0]['origin']['portNumber'])

        self.assertEqual('WARNING', normal_diag[0]['severity'])
        self.assertEqual(20752, normal_diag[0]['message']['code']) ###########
        self.assertEqual('DISAPPEARS', normal_diag[0]['message']['mode'])
        self.assertEqual(master, normal_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, normal_diag[0]['origin']['portNumber'])
         

    def test_ua_undervoltage(self):
        """
        Testet das Verhalten des Aktorausgangs bei Unterspannung 
        und prüft die korrekten Warn- und Entwarnungsereignisse.
        
        
        return: None
        """
                
        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)
        

        tc.set_actuator_voltage(self._under_voltage)
        time.sleep(2)
        undervoltage_diag = dut.get_event()

        tc.set_actuator_voltage(self._nominal_voltage)
        time.sleep(2)
        normal_diag = dut.get_event()


        self.assertEqual('WARNING', undervoltage_diag[0]['severity'])
        self.assertEqual(20753, undervoltage_diag[0]['message']['code']) #############
        self.assertEqual('APPEARS', undervoltage_diag[0]['message']['mode'])
        self.assertEqual(master, undervoltage_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, undervoltage_diag[0]['origin']['portNumber'])

        self.assertEqual('WARNING', normal_diag[0]['severity'])
        self.assertEqual(20753, normal_diag[0]['message']['code']) ##############
        self.assertEqual('DISAPPEARS', normal_diag[0]['message']['mode'])
        self.assertEqual(master, normal_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, normal_diag[0]['origin']['portNumber'])


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


        tc.set_actuator_voltage(self._over_voltage)
        time.sleep(2)
        overvoltage_diag = dut.get_event()

        tc.set_actuator_voltage(self._nominal_voltage)
        time.sleep(2)
        normal_diag = dut.get_event()


        self.assertEqual('WARNING', overvoltage_diag[0]['severity'])
        self.assertEqual(20752, overvoltage_diag[0]['message']['code']) ###########
        self.assertEqual('APPEARS', overvoltage_diag[0]['message']['mode'])
        self.assertEqual(master, overvoltage_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, overvoltage_diag[0]['origin']['portNumber'])

        self.assertEqual('WARNING', normal_diag[0]['severity'])
        self.assertEqual(20752, normal_diag[0]['message']['code']) ###############
        self.assertEqual('DISAPPEARS', normal_diag[0]['message']['mode'])
        self.assertEqual(master, normal_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, normal_diag[0]['origin']['portNumber'])

    
    def test_us_shortcircuit(self):
        """
        Testet das Verhalten bei Kurzschluss der Sensorseite 
        und prüft die korrekten Warn- und Entwarnungsereignisse.
        
        
        return: None
        """

        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)


        tc.peripheral_configuration().ioldevice_bridge_x1_pin1_to_pin3()
        time.sleep(2)
        shortvoltage_diag = dut.get_event()

        tc.peripheral_configuration().ioldevice_bridge_x1_pin1_to_pin3(False)
        time.sleep(2)
        normal_diag = dut.get_event()

        self.assertEqual('ERROR', shortvoltage_diag[0]['severity'])
        self.assertEqual(30480, shortvoltage_diag[0]['message']['code']) ###########
        self.assertEqual('APPEARS', shortvoltage_diag[0]['message']['mode'])
        self.assertEqual(master, shortvoltage_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, shortvoltage_diag[0]['origin']['portNumber'])

        self.assertEqual('ERROR', shortvoltage_diag[0]['severity'])
        self.assertEqual(30480, shortvoltage_diag[0]['message']['code']) ###########
        self.assertEqual('DISAPPEARS', shortvoltage_diag[0]['message']['mode'])
        self.assertEqual(master, shortvoltage_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, shortvoltage_diag[0]['origin']['portNumber'])


    def test_ua_shortcircuit(self):      
        """
        Testet das Verhalten bei Kurzschluss der Aktorseite 
        und prüft die korrekten Warn- und Entwarnungsereignisse.
        
        
        return: None
        """

        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)


        tc.peripheral_configuration().ioldevice_bridge_x5_pin2_to_pin3()
        time.sleep(2)
        shortvoltage_diag = dut.get_event()

        tc.peripheral_configuration().ioldevice_bridge_x5_pin2_to_pin3(False)
        time.sleep(2)
        normal_diag = dut.get_event()

        self.assertEqual('ERROR', shortvoltage_diag[0]['severity'])
        self.assertEqual(30480, shortvoltage_diag[0]['message']['code']) ###########
        self.assertEqual('APPEARS', shortvoltage_diag[0]['message']['mode'])
        self.assertEqual(master, shortvoltage_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, shortvoltage_diag[0]['origin']['portNumber'])

        self.assertEqual('ERROR', shortvoltage_diag[0]['severity'])
        self.assertEqual(30480, shortvoltage_diag[0]['message']['code']) ###########
        self.assertEqual('DISAPPEARS', shortvoltage_diag[0]['message']['mode'])
        self.assertEqual(master, shortvoltage_diag[0]['origin']['masterNumber'])
        self.assertEqual(self._port, shortvoltage_diag[0]['origin']['portNumber'])


    def test_us_input(self):
        """
        Testet das Verhalten, wenn eine Sensorspannung auf einen Eingangspin gesetzt wird.
        Überprüft, ob das System die korrekte Antwort liefert und ob der Pinzustand richtig erkannt wird.


        
        
        return: None
        """
        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)


        tc.peripheral_configuration().ioldevice_bridge_x2_pin1_to_pin2_and_pin4()
        time.sleep(2)
        input_diag = dut.get_processdata_getdata_value()

        tc.peripheral_configuration().ioldevice_bridge_x2_pin1_to_pin2_and_pin4(False)
        time.sleep(2)
        normal_diag = dut.get_processdata_getdata_value

        self.assertEqual(8, input_diag[0]['iolink']['value'][0]) #Wird warscheinlich 8 oder 16 sein...

        self.assertEqual(0, normal_diag[0]['iolink']['value'][0])


    def test_us_ua_connection(self):
        
        """
        Testet das Verhalten, wenn ein Ausgang auf einen Eingangspin gesetzt wird.
        Überprüft, ob das System die korrekte Antwort liefert und ob der Pinzustand richtig erkannt wird.
        
        
        return: None
        """
        tc = get_testcube()
        dut = tc.dut()
        tc.set_sensor_voltage(self._nominal_voltage)
        tc.set_actuator_voltage(self._nominal_voltage)


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


if __name__ == '__main__':
    unittest.main()

