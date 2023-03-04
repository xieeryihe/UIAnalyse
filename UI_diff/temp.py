import os
import re
devices_info = os.popen('adb devices')
devices_info = devices_info.read()
devices = re.findall(r'(.*?)\tdevice\b', devices_info)
print(devices)