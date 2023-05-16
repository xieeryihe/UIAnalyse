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

kanji_info = {
    "packageName": "krillefear.funwithkanji",
    "activityName": ".MainActivity"
}

ruslin_info = {
    "packageName": "org.dianqk.ruslin",
    "activityName": ".MainActivity"
}

# 节拍器
metronome_info = {
    "packageName": "de.moekadu.metronome",
    "activityName": ".MainActivity"
}

calculator_info = {
    "packageName": "com.inator.calculator",
    "activityName": ".activities.MainActivity"
}

bible_info = {
    "packageName": "org.hlwd.bible_multi_the_life",
    "activityName": ".MainActivity"
}

todotree_info = {
    "packageName": "nl.tsmeets.todotree",
    "activityName": ".MainActivity"
}

# 应用名：Minimal
minimaltodo_info = {
    "packageName": "com.rubenroy.minimaltodo",
    "activityName": ".MainActivity"
}

# 应用名：To-Do List
todolist_info = {
    "packageName": "org.secuso.privacyfriendlytodolist",
    "activityName": ".view.SplashActivity"
}

# 天气软件
clima_info = {
    "packageName": "co.prestosole.clima",
    "activityName": "io.flutter.embedding.android.FlutterActivity"
}

# 音效软件
noice_info = {
    "packageName": "com.github.ashutoshgngwr.noice",
    "activityName": ".activity.MainActivity"
}

# 摩尔斯电码
morse_info = {
    "packageName": "rocks.poopjournal.morse",
    "activityName": ".MainActivity"
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

SSIM_threshold = 0.80  # SSIM值超过才认为两张图片相同
HSV_mean_diff_threshold = 7  # HSV平均差异阈值
HSV_peak_diff_threshold = 20  # HSV峰值差异阈值
HSV_peak_per_threshold = 0.05  # HSV峰值差异占比阈值

position_threshold = 0.1  # 位置百分比差距阈值，超过则认为出现UI错误

mis_no = 0  # 失配的图片序号

match_no = 0  # 匹配的图片序号
total_no = 0  # 总共比对的元素数

diff_log = None  # log文件

# 返回值
RET_MISMATCH = -1  # 失配

RET_CLASS_MISMATCH = -3  # 类不一致
RET_TEXT_MISMATCH = -4  # 文本不一致
RET_IMAGE_MISMATCH = -5  # 图像不一致
RET_POSITION_MISMATCH = -6  # 位置不一致

RET_OK = 1  # 没问题
RET_SKIP = 2  # 跳过

RET_REDUNDANCY = -9  # 有节点多余
RET_NODE1_REDUNDANCY = -10  # node1多余
RET_NODE2_REDUNDANCY = -11  # node2多余
