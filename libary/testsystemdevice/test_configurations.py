from powersupply.EaPs2000 import EaPs2000
from relaiscard.Eth008 import Eth800
from .PeripheralConfiguration import PeripheralConfiguration
from .TestCubeBuilder import TestCubeBuilder
from .TestCube import TestCube
from device.JsonRestApi import JsonRestApi

relay_ip_address = "10.10.10.200"
relay_type = Eth800  
power_supply_type = EaPs2000 
power_supply_port = "COM4"
us_channel_port = 0
ua_channel_port = 1
hostname = "192.168.1.6"

def get_testcube() -> TestCube:
    tc = TestCubeBuilder()

    # Set the DUT with the JsonRestApi
    tc.set_dut(JsonRestApi(hostname, 1, 1, ("admin", "private")))

    # Set the power supply with the power supply type and the corresponding port
    tc.set_powersupply(power_supply_type(power_supply_port))

    # Set the relay card with the relay type and the IP address
    tc.set_peripheral_configuration(PeripheralConfiguration(relay_type(relay_ip_address)))

    # Set the US channel
    tc.set_us_channel(us_channel_port)

    # Set the UA channel
    tc.set_ua_channel(ua_channel_port)

    return tc 