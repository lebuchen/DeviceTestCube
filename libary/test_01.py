from device.JsonRestApi import JsonRestApi as jra
import powersupply.PowerSupply as powersupply
import relaiscard.Relaiscard as relaiscard

hostname = "192.168.1.6"
json = jra(hostname, 1, 5, ("admin", "private"))

#print(json.get_processdata_getdata_value())

#Wichtig!!! Es muss noch festgelegt werden, dass der Error nur stimmt, wenn "mode" : "APPEARS"

print(json.get_event(1, 5))

undervoltage_diag = json.get_event(1, 5)

severity = undervoltage_diag[0]['severity']

print(severity)