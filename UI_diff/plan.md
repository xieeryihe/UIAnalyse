现在已经能获取设备信息和列表，能遍历。



同时连接两个设备可行，现在就是要多线程：多线程启动Appium服务，多线程打开APP。



简单点的方法就是：

- 单线程启动Appium
- 多线程分析页面
- 页面分析完之后，再在主线程里对比。

可以先完成单线程