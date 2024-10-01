from device.JsonRestApi import JsonRestApi as jra
import powersupply.PowerSupply as powersupply
import relaiscard.Relaiscard as relaiscard

hostname = "192.168.1.6"
json = jra(hostname, 1, 5, ("admin", "private"))

#print(json.get_processdata_getdata_value()) #diagnose
print(json.get_event(1, 5)) #diagnose