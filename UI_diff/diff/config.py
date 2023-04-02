douYin_packageName = "com.ss.android.ugc.aweme"
douYin_activityName = ".main.MainActivity"

trivia_info = {
    "packageName": "com.example.android.navigation",
    "activityName": ".MainActivity"
}
zhihu_info = {
    "packageName": "com.zhihu.android",
    "activityName": ".app.ui.activity.MainActivity"
}
bilibili_info = {
    "packageName": "tv.danmaku.bili",
    "activityName": ".MainActivityV2"
}

soundrecorder_info = {
    "packageName": "com.danielkim.soundrecorder",
    "activityName": ".activities.MainActivity"
}

caps_example = {
    "platformName": "Android",
    "platformVersion": "9",
    "deviceName": "xxx",
    "appPackage": "com.example.android.navigation",
    "appActivity": ".MainActivity",
    "unicodeKeyboard": True,
    "resetKeyboard": True,
    "noReset": True,
    "newCommandTimeout": 6000,
    "automationName": "UiAutomator2"
}

SSIM_threshold = 0.85  # SSIM值超过才认为两张图片相同

position_threshold = 0.1  # 位置百分比差距阈值，超过则认为出现UI错误

mis_no = 0  # 失配的图片序号

diff_log = None  # log文件

# 返回值
RET_MISMATCH = -1  # 失配
RET_SKIP = -2  # 跳过
RET_OK = 1  # 没问题
