#!/usr/bin/python3
#coding=utf-8

import os
import subprocess
import tempfile

def runShell(cmd):
    '''
    将命令输入到临时文件，并执行，返回执行结果
    '''
    tmpFd, tmpFileName = tempfile.mkstemp()
    os.write(tmpFd, cmd.encode())
    os.close(tmpFd)
    result = execute("bash %s" % (tmpFileName))
    os.remove(tmpFileName)
    print(result)
    print(result.decode())
    return result
    
def execute(cmdStr):
    '''
    执行命令行，返回执行结果（返回 stdout 或 stderr）
    '''
    cmd = cmdStr.split(" ")
    print(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, err = p.communicate()
    return err or stdout

if __name__ == "__main__":
    out = runShell("adb shell 'service call iphonesubinfo 1 | grep -o \"[0-9a-f]\{8\} \"'")
    # out = runShell(r'adb shell \'service call iphonesubinfo 1 | grep -o "[0-9a-f]\{8\} " | tail -n+3 | while read a; do echo -n "\u${a:4:4}\u${a:0:4}"; done\'')
    print(out)