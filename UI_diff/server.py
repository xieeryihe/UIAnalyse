import subprocess


class AppiumServer:
    """封装AppiumServer"""
    cmd = ""


base_port = 4723


def start_server(host="127.0.0.1", port=4723,
                 log_path="./log/appium_log.txt", if_background=False):
    background_property = ""
    if if_background:  # 如果要在后台运行
        background_property = " /b "

    cmd = 'start {} appium -a {} -p {} -bp {} -g {}' \
        .format(background_property, host, port, port + 1, log_path)
    print(cmd)
    subprocess.Popen(cmd, shell=True)


start_server()
