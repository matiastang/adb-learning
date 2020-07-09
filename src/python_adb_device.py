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
    # high_version_imei_str = os.popen("adb shell 'service call iphonesubinfo 1 \| grep -o \"[0-9a-f]\{8\} \" | tail -n+3 | while read a; do echo -n \"\u${a:4:4}\u${a:0:4}\"; done'").read().replace('\n','')
    # os.popen('adb shell')
    # os.popen('su')
    # high_version_imei_str = os.popen('adb shell "service call iphonesubinfo 1 | grep -o \"[0-9a-f]\{8\} \" | tail -n+3 | while read a; do echo -n \"\u${a:4:4}\u${a:0:4}\""').read().replace('\n','')
    # os.popen('exit')
    # pipe_in, pipe_out = os.Popen2('adb shell "service call iphonesubinfo 1"')
    # pipe_in.write('grep -o "[0-9a-f]\{8\} "')
    # pipe_in.write('tail -n+3')
    # pipe_in.write('while read a; do echo -n "\u${a:4:4}\u${a:0:4}"; done')
    # pipe_in.write('\n')#需要换行符
    # pipe_in.flush(); #需要清空缓冲区

    # high_version_imei_str = os.popen('adb shell "service call iphonesubinfo 1"')
    # high_version_imei_str = pipe_out.readline()#读入结果

    # high_version_imei_str = subprocess.call('adb shell \"service call iphonesubinfo 1 | grep -o \"[0-9a-f]\{8\} \" | tail -n+3 | while read a; do echo -n \"\u${a:4:4}\u${a:0:4}\"\"').read().replace('\n','')
    # high_version_imei = high_version_imei_str
    shell = r'adb shell \'service call iphonesubinfo 1 | grep -o "[0-9a-f]\{8\} " | tail -n+3 | while read a; do echo -n "\u${a:4:4}\u${a:0:4}"; done\''
    # high_version_imei = python_run_pipe.runShell(shell)
    print(os.popen(shell))
    high_version_imei = os.popen(shell).read().replace('\n','')
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