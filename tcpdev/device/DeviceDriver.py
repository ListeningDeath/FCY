#-*- coding:utf8 -*-
import socket
import struct


class DeviceDriver:
    def __init__(self):
        host = '192.168.1.126'
        port = 8000
        self.analysis = '15Hh' * 32
        self.destination = (host, port)
        self.client = None

    def startConnect(self):
        """连接板卡 """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(5)
        self.client.connect(self.destination)
        #print 'connect is ok'
        self.client.settimeout(5)

    def setGroupCount(self):
        """设置每帧返回数组数"""
        instruction = [0x00, 0x00, 0x00, 0x00, 0x00, 0x09, 0x01, 0x10, 0x00, 0x14, 0x00, 0x01, 0x02, 0x00, 0x20]
        cmd = struct.pack('15B', instruction[0], instruction[1], instruction[2], instruction[3],
                          instruction[4], instruction[5], instruction[6], instruction[7],
                          instruction[8], instruction[9], instruction[10], instruction[11],
                          instruction[12], instruction[13], instruction[14])
        self.client.sendall(cmd)
        return self.readBack((0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x01, 0x10, 0x00, 0x14, 0x00, 0x01))

    def readBack(self, instruction):
        """验证指令执行成功"""
        data = ''
        while True:
            try:
                data += self.client.recv(1024)
            except socket.timeout:
                #print 'timeout device'
                break
        check_info = struct.unpack('%dB' % len(data), data)
        #print check_info
        if check_info == instruction:
            return True
        else:
            return False

    def reset(self):
        """复位"""
        instruction = [0x00, 0x01, 0x02, 0x03]
        cmd = struct.pack('4b', instruction[0], instruction[1], instruction[2], instruction[3])
        self.client.sendall(cmd)

    def startReceiveData(self, clock=2):
        """开始接收数据1:内时钟2：外时钟"""
        if clock not in [1, 2]:
            raise ValueError('the value must be 1 or 2')
        instruction = [0xff, 0xfe, 0x00, 0x01, clock]
        #print 'receive data', instruction
        cmd = struct.pack('5B', instruction[0], instruction[1], instruction[2], instruction[3], instruction[4])
        self.client.sendall(cmd)

    def stopReceiveData(self):
        """停止数据采集"""
        instruction = [0xff, 0xfe, 0x00, 0x01, 0x00]
        cmd = struct.pack('5B', instruction[0], instruction[1], instruction[2], instruction[3], instruction[4])
        self.client.sendall(cmd)
        #print 'stop has been sended'

    def readData(self):
        """采集数据"""
        #注意收数的超时问题try...except
        data = self.client.recv(1024)
        length = len(data)
        while length < 1024:
            #print 'plus plus plus'
            temp = self.client.recv(1024 - length)
            data += temp
            length = len(data)
        values = struct.unpack(self.analysis, data)
        return values

    def close(self):
            if self.client:
                #self.stopReceiveData()
                self.client.close()
            self.client = None

if __name__ == "__main__":
    driver = DeviceDriver()
    driver.startConnect()
    driver.startReceiveData()



