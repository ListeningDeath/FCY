# -*- coding: utf-8 -*-
from time import sleep
from PySide.QtCore import QObject, Signal
from tcpdev.CommandDevice import CommunicateDevice
import socket
import threading


class MyThread(threading.Thread):
    def __init__(self, callable, *args, **kwargs):
        super(MyThread, self).__init__()
        self.callable = callable
        self.args = args
        self.kwargs = kwargs
        self.lock = threading.RLock()

    def run(self):
        self.callable(*self.args, **self.kwargs)


class TcpLink(QObject):
    #进度条
    signal_progressBar = Signal(int)
    #文本
    signal_noticeText = Signal(str)
    #提示
    signal_tips = Signal(str)
    #LCD显示
    signal_lcd = Signal(tuple)
    #触发
    signal_trigger = Signal()
    #检测结果
    signal_result = Signal(tuple)
    #画图信号
    #signal_draw = Signal()
    #通信超时
    signal_timeout = Signal()

    def __init__(self):
        super(TcpLink, self).__init__()
        self.command = CommunicateDevice()
        self.initValue()

    def initValue(self):
        self.data_pool = []
        self.press_channel = 0
        self.digital_channel = 0
        self.threshold_press = 0.05
        self.init_press = 0.00
        #默认鱼雷
        self.speed_parameter = 0.1018
        self.factor = [10, 10, 10, 10, 10, 10]
        self.calibration = [-0.1, -0.1, -0.1, -0.1, -0.1, -0.1]
        self.running = False
        self.is_online = False
        self.running = False
        self.test_flag = True
        self.trigger_flag = False
        self.clear_flag = False
        self.current_press_flag = False

    def getData(self):
        """获取数据"""
        return self.data_pool[:]

    def clear(self):
        self.data_pool = []

    def getLineState(self):
        return self.command.sendLineState()

    def startConnect(self):
        """进度条，状态信息, 自检结果"""
        def __going():
            #连接函数
            self.signal_progressBar.emit(5)
            #self.signal_tips.emit(u"正在与下位机建立通信中，请勿进行其他操作！")
            #self.signal_noticeText.emit(u"连接中，请稍等......")
            try:
                self.command.startConnect()
            except Exception, e:
                self.signal_result.emit((False, []))
                return
            self.is_online = True
            #print 'no......'
            self.signal_progressBar.emit(30)
            self.signal_noticeText.emit(u"连接成功，系统自检中......")
            #print  self.command.sendClockState() #!= 'CLKSUCCEED':
            #    self.signal_result.emit((False, []))
            #    return
            self.sendSelfTest()
            self.startReceiveData()
            self.keepReading()
            self.signal_progressBar.emit(60)
            self.wait(2)
            self.signal_progressBar.emit(90)
            #此时接收的数据清空，不保留
            self.setClearFlag(True)
            result = self.testData()
            self.clear()
            self.sendReset()
            self.signal_result.emit((True, result))
        worker = MyThread(__going)
        worker.start()

    def keepReading(self):
        """连续读取数据"""
        self.running = True
        self.press_count = 0

        def _read(self):
            end = (0x5a5a, 0x5a5a, 0x5a5a, 0x5a5a, 0x5a5a, 0x5a5a, 0x5a5a, 0x5a5a,
                   0x5a5a, 0x5a5a, 0x5a5a, 0x5a5a, 0x5a5a, 0x5a5a, 0x5a5a, 0x5a5a)
            while self.running:
                try:
                    data = self.command.readData()
                    #print data[-16:]
                    if data[-16:] == end:
                        #print 'end'
                        self.running = False
                        break
                    if not self.test_flag:
                        data = self.netTransform(data)
                        if self.trigger_flag:
                            self.traversalData(data)
                    if not self.clear_flag:
                        self.data_pool.extend(data)
                    if self.current_press_flag:
                        self.press_count += 1
                        if self.press_count >= 10:
                            self.press_count = 0
                            for i in range(6):
                                _data = data[i::16]
                                lcd_value = sum(_data) / 32
                                self.signal_lcd.emit((i, lcd_value))
                    #print self.clear_flag, self.factor
                except socket.timeout:
                    self.signal_timeout.emit()
                    break
                except Exception, e:
                    #print 'except', str(e), 'cannot receive data'
                    break
        worker = MyThread(_read, self)
        worker.start()

    def netTransform(self, data):
        """计算通道实际值"""
        #1--4
        #5--10
        #16
        values = []
        for i in range(32):
            base = i * 16
            #press
            for k, j in enumerate([9, 10, 11, 12, 13, 14]):
                values.append((data[base + j] * (2 ** -20) * 25 - 0.25) * self.factor[k] + self.calibration[k])
            #digital
            for j in [0, 1, 2, 3]:
                values.append((data[base + j] / 65536.0) * 5)
            for j in [4, 5, 6, 7, 8]:
                values.append(data[base + j])
            #speed
            values.append(-data[base + 15] * self.speed_parameter)
        return values

    def setSpeedFactor(self, number):
        if number == 1:
            self.speed_parameter = 0.06135923
        else:
            self.speed_parameter = 0.1018
    def triggered(self):
        """触发启动"""
        self.trigger_flag = False
        self.clear_flag = False
        #print 'triggered'
        self.signal_trigger.emit()

    def traversalData(self, data):
        """
        遍历外部条件触发
        """
        if data:
            if self.traversalDataS(data[15::16]):
                self.triggered()
            elif self.traversalDataP(data[self.press_channel::16]):
                self.triggered()

    def traversalDataS(self, data):
        """速度触发"""
        length = len(data)
        a = sum(data) / length
        if a > 0.25:
            return True
        else:
            return False

    def traversalDataP(self, data):
        """压力触发"""
        length = len(data)
        a = sum(data) / length
        if a >= self.threshold_press + self.init_press:
            return True
        else:
            return False

    def testData(self):
        """
        自检数据
        """
        data = self.getData()
        #for i in range(16):
        #    aa = data[i::16]
        #    print len(aa), 'max:', max(aa), 'min:', min(aa), '::', aa
        pass_sheet = [False] * 11
        channel = [9, 10, 11, 12, 13, 14, 0, 1, 2, 3]
        for i, j in enumerate(channel):
            pool = data[j::16]
            length = len(pool)
            summation = sum(pool)
            if summation > 52000 * length:
                pass_sheet[i] = True
            else:
                #print pool
                pass_sheet[i] = False
        pass_sheet[10] = True
        return pass_sheet

    def setFactor(self, factor):
        """配置系数1,5,10的关系，"""
        self.factor = factor
        print factor

    def setPressChannel(self, channel=0):
        """默认通道"""
        self.press_channel = channel

    def setDigitalChannel(self, channel=0):
        self.digital_channel = channel

    def setThresholdPress(self, press=0.05):
        """ 压力触发值"""
        self.threshold_press = press

    def setInitPress(self, init_press=0.00):
        """ 压力初始值"""
        self.init_press = init_press

    def setCalibration(self, value):
        self.calibration = value

    def setTriggerFlag(self, flag):
        self.trigger_flag = flag

    def setClearFlag(self, flag):
        self.clear_flag = flag

    def setTestFlag(self, flag):
        self.test_flag = flag

    def setCurrentFlag(self, flag):
        self.current_press_flag = flag

    def setReadFlag(self, flag):
        self.command.setReadFlag(flag)

    def sendSelfTest(self):
        self.command.sendSelfTest()

    def sendTigReady(self):
        self.command.sendTigReady()

    def startReceiveData(self):
        self.command.startReceiveData()

    def sendTestResult(self, flag):
        self.command.sendTestResult(flag)

    def sendReset(self):
        self.command.sendReset()

    def wait(self, num):
        self.command.wait(num)

    def waitTrigger(self):
        """等待触发条件"""
        def _read(self):
            trigger = self.command.read()
            #print 'tcplink:', trigger
            if trigger == 'TRIGGER':
                self.triggered()
        worker = MyThread(_read, self)
        worker.start()

    def close(self):
        self.running = False
        if self.is_online:
            self.sendTestResult(False)
            self.command.stopReceiveData()
        self.is_online = False
        self.command.close()
        self.initValue()

if __name__ == "__main__":
    command = TcpLink()
    command.command.startConnect()
    """
    command.startReceiveData()
    command.keepReading()
    sleep(2)
    command.command.stop()
    sleep(1)
    command.close()
    a = command.getData()
    for i in range(16):
        aa = a[i::16]
        print len(aa), 'max:', max(aa), 'min:', min(aa), '::', aa
    """


