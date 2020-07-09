# adb-learning

Android Debug Bridge 安卓调试桥学习

[ADB的常用命令](http://www.aoaoyi.com/archives/738.html)

## 简介

Android Debug Bridge（安卓调试桥） tools。它就是一个命令行窗口，用于通过电脑端与模拟器或者是设备之间的交互。
ADB是一个C/S架构的应用程序，由三部分组成：
1. 运行在pc端的adb client：
命令行程序”adb”用于从shell或脚本中运行adb命令。首先，“adb”程序尝试定位主机上的ADB服务器，如果找不到ADB服务器，“adb”程序自动启动一个ADB服务器。接下来，当设备的adbd和pc端的adb server建立连接后，adb client就可以向ADB servcer发送服务请求；
2. 运行在pc端的adb server：
ADB Server是运行在主机上的一个后台进程。它的作用在于检测USB端口感知设备的连接和拔除，以及模拟器实例的启动或停止，ADB Server还需要将adb client的请求通过usb或者tcp的方式发送到对应的adbd上；管理PC中的Client端和手机的Deamon之间的通信。
3. 运行在设备端的常驻进程adb demon (adbd)：
程序“adbd”作为一个后台进程在Android设备或模拟器系统中运行。它的作用是连接ADB服务器，并且为运行在主机上的客户端提供一些服务。

## 常用命令

* adb version
查看adb版本
```
Android Debug Bridge version 1.0.41
Version 29.0.5-5949299
Installed as /Users/yunxi/android/sdk/platform-tools/adb
```

* adb start-server
启动 `adb server`

* adb kill-server
停止 `adb server`

* adb devices
查询已连接设备/模拟器
```
List of devices attached
FA7540304373	device
```
> 1. offline —— 表示设备未连接成功或无响应；
> 2. device —— 设备已连接；
> 3. no device —— 没有设备/模拟器连接；
> 4. List of devices attached 设备/模拟器未连接到 adb 或无响应

* adb shell

进入调试设备的shell界面, 此时可以使用调试设备中的很多指令. 下文高阶用法中很多就是。`exit`退出。
```
$ adb shell
sailfish:/ $
sailfish:/ $ exit
```

### 安卓系统属性

[python获取测试]()

查询具体系统属性的名字，可以使用grep过滤
```
adb shell getprop | grep product
```
```
[ro.build.product]: [sailfish]
[ro.product.board]: [sailfish]
[ro.product.brand]: [google]
[ro.product.cpu.abi]: [arm64-v8a]
[ro.product.cpu.abilist]: [arm64-v8a,armeabi-v7a,armeabi]
[ro.product.cpu.abilist32]: [armeabi-v7a,armeabi]
[ro.product.cpu.abilist64]: [arm64-v8a]
[ro.product.device]: [sailfish]
[ro.product.first_api_level]: [24]
[ro.product.locale]: [en-US]
[ro.product.manufacturer]: [Google]
[ro.product.model]: [Pixel]
[ro.product.name]: [sailfish]
```
```
#获取手机名称
NAME = 'adb shell getprop ro.product.model'
#获取手机版本
VERSION = 'adb shell getprop ro.build.version.release'
#获取手机厂商
PRODUCER = 'adb shell getprop ro.product.brand'
```

### IMEI

[获取IMEI](http://www.aoaoyi.com/archives/738.html#chapter8.7)
在 Android 4.4 及以下版本可通过如下命令获取 IMEI：
```
adb shell dumpsys iphonesubinfo
```
输出中的Device ID 就是 IMEI

在 Android 5.0 及以上版本里这个命令输出为空，得通过其它方式获取了（需要 root 权限）：
```
$ adb shell
$ su
$ service call iphonesubinfo 1
```
```
sailfish:/ $ su
sailfish:/ # service call iphonesubinfo 1
Result: Parcel(
  0x00000000: 00000000 0000000f 00350033 00350032 '........3.5.2.5.'
  0x00000010: 00310033 00380030 00320035 00380038 '3.1.0.8.5.2.8.8.'
  0x00000020: 00380036 00000034                   '6.8.4...        ')
```
把里面的有效内容提取出来就是 IMEI 了，比如这里的是 352531085288648。

## adb connect/disconnect

[Android adb](https://www.jianshu.com/p/5980c8c282ef)

通过wifi进行远程连接手机进行调试的.
[wifi调试](https://link.jianshu.com/?t=https://developer.android.com/studio/command-line/adb.html#wireless)
需先连上usb模式, 开启远程调试模式:
```
$ adb tcpip 5555
```