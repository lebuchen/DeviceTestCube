from relaiscard.Relaiscard import RelaisCard

'''
Was kann hier angepasst werden?
MKVPro
1. X3 Pin 1 zu Pin 3 (Kurzschluss Sensorversorgung)
2. X4 Pin 1 zu Pin 4 (Eingang Pin 4)
3. X5 Pin 1 zu Pin 2 (Eingang Pin 2)
4. X6 Pin 4 zu Pin 3 (Kurzschluss Ausgang Pin 4)
5. X7 Pin 2 zu Pin 3 (Kurzschluss Ausgang Pin 2)

IO-Link Device 55518
6. X1 Pin 1 zu Pin 3 (Kurzschluss Sensorversorgung)
7. X2 Pin 1 zu Pin 2 und Pin 4 (Eingang Pin 2 und Pin 4)
8. X5 Pin 2 zu Pin 3 (Kurzschluss Ausgang Pin 2)
'''

class PeripheralConfiguration:
    relais_mvkpro_bridge_x3_pin1_to_pin3 = 8
    relais_mvkpro_bridge_x4_pin1_to_pin4 = 1
    relais_mvkpro_bridge_x5_pin1_to_pin2 = 2
    relais_mvkpro_bridge_x6_pin4_to_pin3 = 7
    relais_mvkpro_bridge_x7_pin2_to_pin3 = 6
    relais_ioldevice_bridge_x1_pin1_to_pin3 = 5
    relais_ioldevice_bridge_x2_pin1_to_pin2_and_pin4 = 3
    relais_ioldevice_bridge_x5_pin2_to_pin3 = 4


    def __init__(self, relaiscard: RelaisCard) -> None:
        self._relaiscard = relaiscard

        #Apply default configuration
        #MVK
        self.mvkpro_bridge_x3_pin1_to_pin3(False)
        self.mvkpro_bridge_x4_pin1_to_pin4()
        self.mvkpro_bridge_x5_pin1_to_pin2()
        #May lead to short circuit of output to ground
        self.mvkpro_bridge_x6_pin4_to_pin3(False)
        #May lead to short circuit of output to ground
        self.mvkpro_bridge_x7_pin2_to_pin3(False)

        #Hub
        #May lead to short circuit of supply voltage to ground
        self.ioldevice_bridge_x1_pin1_to_pin3(False)
        self.ioldevice_bridge_x2_pin1_to_pin2_and_pin4()
        #May lead to short circuit of output to ground
        self.ioldevice_bridge_x5_pin2_to_pin3(False)


    def mvkpro_bridge_x3_pin1_to_pin3(self, bridge: bool = True):
        self._relaiscard.set_relais_state(self.relais_mvkpro_bridge_x3_pin1_to_pin3, bridge)

    def mvkpro_bridge_x4_pin1_to_pin4(self, bridge: bool = True):
        self._relaiscard.set_relais_state(self.relais_mvkpro_bridge_x4_pin1_to_pin4, bridge)

    def mvkpro_bridge_x5_pin1_to_pin2(self, bridge: bool = True):
        self._relaiscard.set_relais_state(self.relais_mvkpro_bridge_x5_pin1_to_pin2, bridge)

    def mvkpro_bridge_x6_pin4_to_pin3(self, bridge: bool = True):
        self._relaiscard.set_relais_state(self.relais_mvkpro_bridge_x6_pin4_to_pin3, bridge)

    def mvkpro_bridge_x7_pin2_to_pin3(self, bridge: bool = True):
        self._relaiscard.set_relais_state(self.relais_mvkpro_bridge_x7_pin2_to_pin3, bridge)

    def ioldevice_bridge_x1_pin1_to_pin3(self, bridge: bool = True):
        self._relaiscard.set_relais_state(self.relais_ioldevice_bridge_x1_pin1_to_pin3, bridge)

    def ioldevice_bridge_x2_pin1_to_pin2_and_pin4(self, bridge: bool = True):
        self._relaiscard.set_relais_state(self.relais_ioldevice_bridge_x2_pin1_to_pin2_and_pin4, bridge)

    def ioldevice_bridge_x5_pin2_to_pin3(self, bridge: bool = True):
        self._relaiscard.set_relais_state(self.relais_ioldevice_bridge_x5_pin2_to_pin3, bridge)
