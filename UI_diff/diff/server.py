import subprocess


class AppiumServer:
    """
    封装AppiumServer
    SAP中的元素为字典，一般格式如下：
    {
        "host": self.host,
        "port": temp_port
    }
    """
    host = "127.0.0.1"
    base_port = 4723
    SAP_list = []  # 服务访问点（service access point）列表

    def __init__(self):
        pass

    @staticmethod
    def start_server(host=host, port=base_port, uid="emulator-5554", if_background=False):
        background_property = ""
        log_path = "./log/appium_log_{}.txt".format(port)
        if if_background:  # 如果要在后台运行
            background_property = " /b "

        cmd = 'start {} appium -a {} -p {} -bp {} -g {} -U {}' \
            .format(background_property, host, port, port + 1, log_path, uid)
        print(cmd)
        subprocess.Popen(cmd, shell=True)

    def start_servers(self, server_num=1, devices_dict=None, if_background=False ):
        for i in range(0, server_num):
            temp_port = self.base_port + i * 2
            uid = devices_dict[i]["deviceName"]
            self.start_server(host=self.host, port=temp_port, uid=uid,
                              if_background=if_background)
            temp_dict = {
                "host": self.host,
                "port": temp_port,
                "deviceName": uid
            }
            self.SAP_list.append(temp_dict)
        return self.SAP_list
