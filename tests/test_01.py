import libary.device as device
import libary.powersupply as powersupply
import libary.relaiscard as relaiscard

import platform

hostname = platform.uname().node

json = device.JsonRestApi(hostname, 1, 1, None)
print(json.get_processdata_value())
