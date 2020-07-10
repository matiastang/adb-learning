#!/usr/bin/python3
#coding=utf-8

def isImei(imei):
    '''
    验证规则
    1.区分imei的奇数位和偶数位。
    2.奇数位相加。
    3.偶数位乘以2，若小于10则直接相加，大于10则对十位数和个位数进行相加。
    4.奇数位相加之和与第3步逻辑只和相加，获取到一个数字。
    5.得到的数字与10进行取余，余数若为0，则验证位数字为0，若余数不为0，则验证位为(10-余数)。
    '''
    try:
        imeiChar = list(imei)  # .toCharArray()
        resultInt = 0
        i = 0
        while i < len(imeiChar) - 1:
            a = int(imeiChar[i])
            i += 1
            temp = int(imeiChar[i]) * 2
            b = (temp - 9, temp)[temp < 10]  # temp if temp < 10 else temp - 9
            resultInt += a + b
            i += 1
        resultInt %= 10
        resultInt = (10 - resultInt, 0)[resultInt == 0]
        crc = int(imeiChar[14])
        return resultInt == crc
    except:
        return False

if __name__ == "__main__":
    print('方法isImei检测是否为imei')