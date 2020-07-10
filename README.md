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
[python cmd 获取imei](https://stackoverflow.com/questions/27002663/adb-shell-dumpsys-iphonesubinfo-not-working-since-android-5-0-lollipop)
在 Android 4.4 及以下版本可通过如下命令获取 IMEI：
```
adb shell dumpsys iphonesubinfo
```
输出中的Device ID 就是 IMEI

adb shell getprop gsm.baseband.imei

在 Android 5.0 及以上版本里这个命令输出为空，得通过其它方式获取了（需要 root 权限）：
```
$ adb shell
$ su
$ service call iphonesubinfo 1
```
或
```
adb shell service call iphonesubinfo 1
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
或者您可以使用此Windows单行程序在设备端执行此操作：
```
adb shell "service call iphonesubinfo 1 | grep -o '[0-9a-f]\{8\} ' | tail -n+3 | while read a; do echo -n \\u${a:4:4}\\u${a:0:4}; done"
```
或者在Linux中：
```
adb shell 'service call iphonesubinfo 1 | grep -o "[0-9a-f]\{8\} " | tail -n+3 | while read a; do echo -n "\u${a:4:4}\u${a:0:4}"; done'

adb shell service call iphonesubinfo 1 | awk -F "'" '{print $2}' | sed '1 d' | tr -d '.' | awk '{print}' ORS=
```
```py
import os

def device_imei():
    version = device_version()
    if (version < '4.4'):
        low_version_imei = os.popen('adb shell dumpsys iphonesubinfo').read().replace('\n','')
        print('低版本(<= 4.4)imei: %s'% low_version_imei)
        return low_version_imei
    high_version_imei_str = os.popen(r"""adb shell service call iphonesubinfo 1 | awk -F "'" '{print $2}' | sed '1 d' | tr -d '.' | awk '{print}' ORS=""").read()
    high_version_imei = high_version_imei_str.replace(' ','')
    return high_version_imei
```

## adb connect/disconnect

[Android adb](https://www.jianshu.com/p/5980c8c282ef)

通过wifi进行远程连接手机进行调试的.
[wifi调试](https://link.jianshu.com/?t=https://developer.android.com/studio/command-line/adb.html#wireless)
需先连上usb模式, 开启远程调试模式:
```
$ adb tcpip 5555
```

1、获取手机系统信息（ CPU，厂商名称等）
adb shell "cat /system/build.prop | grep "product""

2、获取手机系统版本
adb shell getprop ro.build.version.release

3、获取手机系统api版本
adb shell getprop ro.build.version.sdk

4、获取手机设备型号
adb -d shell getprop ro.product.model

5、获取手机厂商名称
adb -d shell getprop ro.product.brand

6、获取手机的序列号
有两种方式

1、  adb get-serialno

2、  adb shell getprop ro.serialno


 

7、获取手机的IMEI
有三种方式，由于手机和系统的限制，不一定获取到

1、 adb shell dumpsys iphonesubinfo

其中Device ID即为IMEI号

2、 adb shell getprop gsm.baseband.imei

3、 service call iphonesubinfo 1 

此种方式，需要自己处理获取的信息得到

8、获取手机mac地址

adb shell cat /sys/class/net/wlan0/address

9、获取手机内存信息
adb shell cat /proc/meminfo

10、获取手机存储信息
adb shell df

获取手机内部存储信息：

魅族手机： adb shell df /mnt/shell/emulated

其他： adb shell df /data

获取sdcard存储信息：

adb shell df /storage/sdcard

11、获取手机分辨率
adb shell "dumpsys window | grep mUnrestrictedScreen"

12、获取手机物理密度
adb shell wm density

 

adb shell input text

输入一个字符串,只支持英文数字和部分符号
当需要为一个控件输入内容时,需要先保证输入框正片处于焦点

adb shell dumpsys activty | grep -i mSleeping

判断当前屏幕状态

adb shell dumpsys cpuinfo

adb shell top -s cpu

获取手机cpu信息

adb shell am start packageName/className

启动一个Activity

adb shell am broadcast

发送一个广播,使用-a来指定Action,-d指定数据

  adb shell am broadcast -a 'com.icechao.broadcast'
adb shell am am force-stop packageName

强制停止一个应用

adb shell pm clear packageName

清理应用数据

adb shelll kill pid

杀死某个进程

adb logcat -v time -d

打印logcat

adb shell df

文件系统的磁盘空间占用情况

adb shell /system/bin/screencap -p /sdcard/screenshot.png

手机截屏

adb shell screenrecord --time-limit 10 /sdcard/demo.mp4

录制屏幕

adb shell getprop dhcp.wlan0.ipaddress

获取手机ip地址

cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq

获取手机Cpu最小频率

cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq

获取手机Cpu最大频率

cat /sys/devices/system/cpu/cpu0/cpufreq/kernel_max

获取手机cpu核数

adb shell dumpsys window policy | grep mScreenOnFully

获取手机屏幕策略,windows中需要不能使用grep命令筛选信息

adb shell dumpsys window policy | grep mShowingLockscreen

判断当前手机是否是锁屏状态

adb shell svc wifi enable/disable

   打开手机wifi,实测部份三星手机不支持些方法
adb shell monkey

能过monkey植入事件为app进行压力测试

grep(命令中 ' | '到命名结束的部份)命令可以从得到的结果里筛选想要的信息行,这个命令只支持linux 在windows可以考虑使用findstr

在进入手机shell模式后很多通用命令是和linux是一样的,所以可以直接使用linux命令来获取手机的信息

当电脑连接多台手机使用 adb -s 手机序列号 命令 的方式指定手机

 

adb shell intput swipe left top right bottom

植入屏幕滑动事件
左上为滑动的起始位置,右下为滑动的结束位置
adb shell input swipe 100 200 500 300

 

adb shell input tap

植入屏幕点击事件,先X轴再Y轴

  adb shell input tap 100 200