from diff.devices import *

if __name__ == '__main__':
    devices = Devices()
    devices.start_drivers(trivia_info)
    devices.compare_test()
    devices.stop_drivers()

