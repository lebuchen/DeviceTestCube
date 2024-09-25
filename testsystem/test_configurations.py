from platform import uname
from mvkpro import MvkPro, NpxConnection
from powersupply import EaPs2000, Hcs3202
from relaiscard import Eth800
from .PeripheralConfiguration import PeripheralConfiguration
from .TestCubeBuilder import TestCubeBuilder
from .TestCube import TestCube

def get_testcube() -> TestCube:
    hostname = uname().node

    #configuration for TestCube MOCHA-MURR-01 (PNIO)
    if hostname == "DEOPP-MA101813":
        return TestCubeBuilder()\
            .set_dut(MvkPro(NpxConnection("10.10.10.100")))\
            .set_relaiscard(Eth800("10.10.10.200"))\
            .set_powersupply(Hcs3202("COM4"))\
            .set_us_channel(0)\
            .get_testcube()
    
    #configuration for Steffens new Laptop
    elif hostname == "DEOPP-NB102277":
        return TestCubeBuilder()\
            .set_dut(MvkPro(NpxConnection("192.168.1.4")))\
            .set_powersupply(EaPs2000("COM3"))\
            .set_us_channel(0)\
            .set_ua_channel(1)\
            .get_testcube()
        
    #configuration for Testcube with 54600    
    elif hostname == "DEOPP-PC102326":
        return TestCubeBuilder()\
            .set_dut(MvkPro(NpxConnection("192.168.1.2")))\
            .set_powersupply(EaPs2000("COM3"))\
            .set_us_channel(0)\
            .set_ua_channel(1)\
            .set_peripheral_configuration(PeripheralConfiguration(Eth800("192.168.1.200")))\
            .get_testcube()
                
    #configuration for Benedikt   
    elif hostname == "DEOPP-NB102568":
        return TestCubeBuilder()\
            .set_dut(MvkPro(NpxConnection("192.168.1.12")))\
            .set_powersupply(EaPs2000("COM3"))\
            .set_us_channel(0)\
            .set_ua_channel(1)\
            .get_testcube()

    else:
        raise Exception(f"no valid testcube configuration for host {hostname} found")
