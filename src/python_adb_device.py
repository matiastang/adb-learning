#!/usr/bin/python3
#coding=utf-8

import os

def device_info():
    deviceName = os.popen('adb shell getprop ro.product.model').read()
    print('手机名称: %s' % deviceName)
    platformVersion = os.popen('adb shell getprop ro.build.version.release').read()
    print('手机版本: %s' % platformVersion)
    device = os.popen('adb shell getprop ro.product.name ').read()
    print('手机厂商: %s' % device)

if __name__ == "__main__":
    device_info()