from powersupply.EaPs2000 import EaPs2000
from relaiscard.Eth008 import Eth800
from .PeripheralConfiguration import PeripheralConfiguration
from .TestCubeBuilder import TestCubeBuilder
from .TestCube import TestCube
from device.JsonRestApi import JsonRestApi

#DUT-config
dut_type = JsonRestApi
hostname = "192.168.1.6"
master = 1
port = 1

#relay-config
relay_ip_address = "10.10.10.200"
relay_type = Eth800  

#powersupply-config
power_supply_type = EaPs2000 
power_supply_port = "COM4"

#channel-config
us_channel_port = 0
ua_channel_port = 1


def get_testcube() -> TestCube:

    return TestCubeBuilder()\
    .set_dut(dut_type(hostname, master, port, ("admin", "private")))\
    .set_us_channel(us_channel_port)\
    .set_ua_channel(ua_channel_port)\
    .get_testcube()
    
    # return TestCubeBuilder()\
    #     .set_dut(dut_type(hostname, master, port, ("admin", "private")))\
    #     .set_powersupply(power_supply_type(power_supply_port))\
    #     .set_peripheral_configuration(PeripheralConfiguration(relay_type(relay_ip_address)))\
    #     .set_us_channel(us_channel_port)\
    #     .set_ua_channel(ua_channel_port)\
    #     .get_testcube()
    
