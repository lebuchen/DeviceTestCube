import unittest
from testsystemdevice.test_configurations import get_testcube


class UsUaDiags:
    def test_us_nodervoltage(self):
        tc = get_testcube()
        dut = tc.dut()
        print(dut.get_event())


test = UsUaDiags()

test.test_us_nodervoltage()

# if __name__ == '__main__':
#     unittest.main()

 
