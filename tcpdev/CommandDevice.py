#-*- coding:utf8 -*-
########################################################################################################################
#clear() 清空数据池
#getData() 获取数据
#startConnect() 建立连接
import socket
from time import sleep
from device.DeviceDriver import DeviceDriver


class CommunicateDevice:
    def __init__(self):
        self.device = DeviceDriver()
        self.read_flag = False
        self.client = None

    def startConnect(self):
        """建立连接"""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(5)
        self.device.startConnect()
        self.client.connect(('192.168.1.178', 4001))

    def setFrameGroup(self):
        """设置返回的数据组数"""
        if not self.device.setGroupCount():
            print 'failed'

    def startReceiveData(self):
        """采集数据指令"""
        self.device.startReceiveData()

    def stopReceiveData(self):
        self.device.stopReceiveData()

    def readData(self):
        """读取板卡实时数据"""
        return self.device.readData()

    def stop(self):
        """停止数据接收"""
        self.device.stopReceiveData()

    def wait(self, num):
        sleep(num)

    def read(self):
        """读取命令数据"""
        buf = ''
        self.read_flag = True
        while self.read_flag:
            try:
                data = self.client.recv(1024)
                #print 'every:', data
                buf += data
                if data.endswith('\n'): # ends with \n
                    self.read_flag = False
                    break
            except socket.timeout:
                if self.read_flag:
                    #print 'continue'
                    continue
                else:
                    #print 'break'
                    break
            except Exception, e:
                buf = 'N/A'
                #print buf
                break
        buf = buf.strip('#')
        cmm = buf.split('\n')
        return cmm[0]

    def send(self, cmd):
        """
        发送指令
        """
        self.client.send('#' + cmd + '\n')

    def sendSelfTest(self):
        """
        通知下位机，自检
        """
        self.send('SELFTEST')
        self.wait(2)

    def sendTestResult(self, passState):
        """
        通知下位机是否自检通过
        """
        if passState:
            self.send('TESTPASSED')
        else:
            self.send('TESTFAILED')

    def sendLineState(self):
        """
        检查线路匹配状态
        """
        self.send('LINESTATUE')
        return self.read()

    def sendReset(self):
        self.send('RESET')
        self.sendTestResult(True)

    def sendClockState(self):
        """
        检查时钟状态
        """
        self.send('CLOCKSTA')
        return self.read()

    def sendTigReady(self):
        """可以进行触发监听"""
        self.send('TIGREADY')

    def deviceReset(self):
        self.device.reset()

    def setReadFlag(self, flag):
        self.read_flag = flag

    def close(self):
        if self.client:
            self.device.close()
            self.client.close()
        self.client = None

if __name__ == "__main__":
    command = CommunicateDevice()
    command.startConnect()
    #command.setFrameGroup()
    """
    command.startReceiveData()
    command.keepReading()
    sleep(4)
    command.stop()

    i = 0
    while i < 5:
        print i, len(command.getData()) / 16.0
        sleep(1)
        i += 1
    command.close()

    sleep(2)
    a = command.getData()
    for i in range(16):
        aa = a[i::16]
        print len(aa), 'max:', max(aa), 'min:', min(aa), '::', aa
    """
    for i in range(15):
        command.sendClockState()
        sleep(2)
    command.close()






