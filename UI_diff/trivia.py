from devices import *

if __name__ == '__main__':
    devices = Devices()
    devices.start(trivia_info)
    devices.compare_test()
    devices.stop()

