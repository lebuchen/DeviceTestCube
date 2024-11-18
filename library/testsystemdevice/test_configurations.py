from library.powersupply.EaPs2000 import EaPs2000
from library.relaiscard.Eth008 import Eth800
from .PeripheralConfiguration import PeripheralConfiguration
from .TestCubeBuilder import TestCubeBuilder
from .TestCube import TestCube
from library.device.JsonRestApi import JsonRestApi
import time


"var auslagen in extra dateien die man auswählen kann und den pfad übergibt?"

#DUT-config
dut_type = JsonRestApi
hostname = "192.168.1.111"
master = 1
port = 3

#relay-config
relay_type = Eth800  
relay_ip_address = "192.168.1.200"


#powersupply-config
power_supply_type = EaPs2000 
power_supply_port = "COM3"

#channel-config
us_channel_port = 1
ua_channel_port = 0


def get_testcube() -> TestCube:
    # start = power_supply_type(power_supply_port)
    # start.set_voltage(24.0, 0)
    # start.set_voltage(24.0, 1)
    # start.set_output_active
    # time.sleep(5)
    
    return TestCubeBuilder()\
        .set_dut(dut_type(hostname, master, port, ("admin", "private")))\
        .set_powersupply(power_supply_type(power_supply_port))\
        .set_peripheral_configuration(PeripheralConfiguration(relay_type(relay_ip_address)))\
        .set_us_channel(us_channel_port)\
        .set_ua_channel(ua_channel_port)\
        .get_testcube()

    # return TestCubeBuilder()\
    #     .set_dut(dut_type(hostname, master, port, ("admin", "private")))\
    #     .set_powersupply(power_supply_type(power_supply_port))\
    #     .set_us_channel(us_channel_port)\
    #     .set_ua_channel(ua_channel_port)\
    #     .get_testcube()
    

    
