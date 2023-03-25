from diff.devices import *

if __name__ == '__main__':
    devices = Devices()

    devices.start_drivers(trivia_info)
    # devices.compare_test()
    # devices.test_single()
    # devices.compare_two_page()
    devices.stop_drivers()

