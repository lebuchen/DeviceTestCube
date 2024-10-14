from device.JsonRestApi import JsonRestApi as jra
import powersupply.PowerSupply as powersupply
from relaiscard.Eth008 import Eth800

hostname = "192.168.1.111"
json = jra(hostname, 1, 2, ("admin", "private"))

print(json.get_event(1, 2))

#undervoltage_diag = json.get_event(1, 5)

#severity = undervoltage_diag[0]['severity']

#print(severity)

# from powersupply.EaPs2000 import EaPs2000

# ea = EaPs2000("COM3")
# ea.set_voltage(24.1, 1)
# ea.set_output_active(True)
