# -*- coding: utf-8 -*-
import numpy as np


class HandleData:
    def __init__(self, speed_data=None, distance=0.48):
        self.speed_data = speed_data
        self.length = len(speed_data)
        #print self.length, 'changdu'
        self.distance = distance

    def shift(self):
        """shift"""
        shift_data = []
        for i, j in enumerate(self.speed_data):
            if i > 0:
                temp = shift_data[-1] + j * 5E-4
                shift_data.append(temp)
            else:
                shift_data.append(0)
        return shift_data

    def acceleration(self):
        """acceleration"""
        acceleration_data = []
        for i, j in enumerate(self.speed_data):
            if i > 0:
                temp = (self.speed_data[i] - self.speed_data[i - 1]) * 200
                acceleration_data.append(temp)
            else:
                acceleration_data.append(0)
        return self.smooth(acceleration_data, 48)

    def getShiftAcceleration(self):
        """
        both
        """
        shift = []
        acceleration = []
        for i, j in enumerate(self.speed_data):
            if i > 0:
                shift.append(shift[-1] + j * 5E-4)
                acceleration.append((self.speed_data[i] - self.speed_data[i - 1]) * 200)
            else:
                shift.append(0)
                acceleration.append(0)
        acceleration = self.smooth(acceleration, 200)
        return (shift, acceleration)

    def getStartTime(self):
        """start time"""
        length = len(self.speed_data)
        for i, j in enumerate(self.speed_data):
            if j > 0 and length - i > 10:
                for j in range(10):
                    if self.speed_data[i + j] > 0:
                        if j == 9:
                            return i
                    else:
                        break
        return length - 1

    def getOutTime(self, shift_data):
        """出管时间点"""
        for i, j in enumerate(shift_data):
            if j >= self.distance:
                return i
        return self.length - 1

    def getStopTime(self, shift_data, distance):
        """出管点时间"""
        #求得最大值
        value = max(shift_data)
        if  value > distance:
            value = distance
        for i, j in enumerate(shift_data):
            if j >= value:
                return i
        return len(shift_data) - 1

    def smooth(self, x, window_len = 10, window = 'flat'):
        """
        曲线平滑
        """
        s=np.r_[x, x[-1:-window_len:-1]]
        if window == 'flat':
            w=np.ones(window_len,'d')
        if len(s) == 0:
            return s
        y=np.convolve(w/w.sum(),s,mode='valid')
        return y

    def bleedTime(self, digital_data):
        """泄放时间"""
        count = 0
        flag = False
        length = len(digital_data)
        for i in range(length):
            #for test
            if digital_data[i] < 2.5:
            #real thing for company
            #if digital_data[i] > 2.5:
                count += 1
                if count >= 4000:
                    flag = True
            else:
                if flag:
                    return count
                count = 0
        return count

    def getStartClock(self, digital_data):
        """开启时机"""
        count = 0
        flag = False
        for i, j in enumerate(digital_data):
            #for test
            if j < 2.5:
            #real thing for company
            #if j > 2.5:
                count += 1
                if count >= 4000:
                    flag = True
            else:
                if flag:
                    return (count, i - count)
                count = 0
        return (count, i - count)

    def setChamberPressure(self, press_data, init_data):
        for i, j in enumerate(press_data):
            press_data[i] = j - init_data

    def getTriggerTime(self, digital_data1):
        #只用于检测1通道的发射时间和延迟时间
        count = 0
        for i, j in range(digital_data1):
            if j > 3:
                count += 1
                if count >= 10:
                    return i - count
            else:
                count = 0
        return i

if __name__ == "__main__":
    import sys
    reportdata = {'SERIAL':'123456','TYPE':'鱼雷','TRIGGER':'手动触发','PERSON':'测试人员','DATE':'20120909',\
                  'PRESS':{1:'00.00',2:'00.00',3:'00.00',4:'00.00',5:'00.00',6:'00.00'},\
                  'DIGITAL':{1:('00.00','20.00'),2:('00.00','20.00'),3:('00.00','20.00'),\
                  4:('00.00','20.00')},'ACCELERATION':'00.00','SPEED':'00.00','DELAY':'00.00',\
                  'SHOOT':'00.00','OPEN':'00.00','BLEED':'00.00','DEEP':'00.0'}
    report = HandleData([])
    press_name = ['','','','','','']
    digital_name = ['','','','']
    a = report.generateReport3(reportdata, press_name, digital_name,'')
    f = open("h:/aa.html",'w')
    f.write(a)
    f.close()


