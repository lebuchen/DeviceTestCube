
from device.JsonRestApi import JsonRestApi as jra
import powersupply as powersupply
import relaiscard as relaiscard


hostname = "192.168.1.6"


json = jra(hostname, 1, 1)
print(json.get_processdata_value())



