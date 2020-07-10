#!/usr/bin/python3
#coding=utf-8

import os
import subprocess

import python_run_pipe

def device_version():
    platformVersion = os.popen('adb shell getprop ro.build.version.release').read().replace('\n','')
    print('版本: %s' % platformVersion)
    return platformVersion

def device_imei():
    version = device_version()
    if (version < '4.4'):
        low_version_imei = os.popen('adb shell dumpsys iphonesubinfo').read().replace('\n','')
        print('低版本(<= 4.4)imei: %s'% low_version_imei)
        return low_version_imei
    # high_version_imei_str = os.popen(r"""adb shell 'service call iphonesubinfo 1 | grep -o "[0-9a-f]\{8\} " | tail -n+3 | while read a; do echo -n "\u${a:4:4}\u${a:0:4}"; done'""").read()
    # print(high_version_imei_str)
    # high_version_imei_str = high_version_imei_str.replace('\x00','')
    # print(high_version_imei_str)
    # [python cmd 获取 imei](https://stackoverflow.com/questions/27002663/adb-shell-dumpsys-iphonesubinfo-not-working-since-android-5-0-lollipop)
    high_version_imei_str = os.popen(r"""adb shell service call iphonesubinfo 1 | awk -F "'" '{print $2}' | sed '1 d' | tr -d '.' | awk '{print}' ORS=""").read()
    # print(high_version_imei_str)
    # high_version_imei_str = high_version_imei_str.replace(' ','')
    # print(high_version_imei_str)
    high_version_imei = high_version_imei_str.replace(' ','')
    return high_version_imei

def device_info():

    version = device_version()
    print('version: %s' % version)

    imei = device_imei()
    print('imei: %s'% imei)

    deviceName = os.popen('adb shell getprop ro.product.model').read()
    print('手机名称: %s' % deviceName)

    device = os.popen('adb shell getprop ro.product.name ').read()
    print('手机厂商: %s' % device)



if __name__ == "__main__":
    device_info()