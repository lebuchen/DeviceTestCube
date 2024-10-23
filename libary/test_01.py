from device.JsonRestApi import JsonRestApi as jra
import powersupply.PowerSupply as powersupply
from relaiscard.Eth008 import Eth800
import time


hostname = "192.168.1.111"
json = jra(hostname, 1, 3, ("admin", "private"))
eth = Eth800("192.168.1.200")
eth.set_relais_state(3, True)
time.sleep(1)  #Statt Timer Statusabfrage

#print(json.get_device_port(1,3,4))

print(json.post_processdata_value(True, None , [0, 3] , True, 1, 3 ))
input_diag = json.get_processdata_getdata_value()
# print(json.post_processdata_value(False, None , [0, 0] , False, 1, 3 ))
#print(json.get_processdata_getdata_value())
#print(json.get_processdata_value())
x= json.get_event
print(x)
print(input_diag)
print(input_diag['iolink']['value'][1])

eth.set_relais_state(3, False)

time.sleep(5)  #Statt Timer Statusabfrage

# print(json.get_processdata_value())
# print(json.get_event())

#index: int, subindex: int = None, master: int = None, port: int = None

# hostname = "192.168.1.111"
# json = jra(hostname, 1, 3, ("admin", "private"))

# print(json.get_event())

# #undervoltage_diag = json.get_event(1, 5)

# #severity = undervoltage_diag[0]['severity']

# #print(severity)

# # from powersupply.EaPs2000 import EaPs2000

# # ea = EaPs2000("COM3")
# # ea.set_voltage(24.1, 1)
# # ea.set_output_active(True)
