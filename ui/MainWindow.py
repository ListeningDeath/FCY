# -*- coding: utf-8 -*-
from PySide.QtGui import QHBoxLayout, QMainWindow, QMessageBox, QPrinter, QTextDocument, QPrintDialog, QPainter,QFont, \
    QFontMetrics, QFileDialog, QVBoxLayout
from PySide.QtCore import SIGNAL, QTimer, Qt
from Ui_MainWindow import Ui_MainWindow
from NoticeWidget import NoticeWidget
from CurveWidget import CurveWidget
from Explain import Explain
from Configuration import Configuration
from LCDGroup import LCDGroup
from lib.TcpLink import TcpLink
from ConfigDialog import ConfigDialog
from lib.HandleData import HandleData
import os, datetime


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(960, 640)
        #不会出现对toolbar的隐藏
        self.toolBar.toggleViewAction().setVisible(False)
        self.finishingLayout()
        self.setupValue()
        self.setupSignal()
        self.setupAction(config=False, start=False, reset=False, result=False, printer=False, back=False)
        self.setShow(1)
        self.setShow(3)

    def setupValue(self):
        self.__action = {"config": False, "start": False, "reset": False,
                         "result": False, "print": False, "back": False, "exit": True}
        self.color_sheet = ['#0000ff', '#ff0000', '#ffff00', '#00ff40', '#00ffff', '#0080c0', '#8080c0',
                            '#ff00ff', '#800000', '#ff8000', '#008040', '#800080', 'black']
        self.lcd_group = [self.lcd_window.press_lcd1, self.lcd_window.press_lcd2, self.lcd_window.press_lcd3,
                          self.lcd_window.press_lcd4, self.lcd_window.press_lcd5, self.lcd_window.press_lcd6,
                          self.lcd_window.digital_lcd1, self.lcd_window.digital_lcd2, self.lcd_window.digital_lcd3,
                          self.lcd_window.digital_lcd4, self.lcd_window.speed_lcd, self.lcd_window.acceleration_lcd,
                          self.lcd_window.shift_lcd]
        self.chk_group = [self.lcd_window.press_chk1, self.lcd_window.press_chk2, self.lcd_window.press_chk3,
                          self.lcd_window.press_chk4, self.lcd_window.press_chk5, self.lcd_window.press_chk6,
                          self.lcd_window.digital_chk1, self.lcd_window.digital_chk2, self.lcd_window.digital_chk3,
                          self.lcd_window.digital_chk4, self.lcd_window.speed_chk, self.lcd_window.acceleration_chk,
                          self.lcd_window.shift_chk]
        self.tcp_link = TcpLink()
        #比例转换系数1,5,10
        self.scaleRegion = (40, 10, 5, 2, 1)
        self.scaleFactor = [10, 10, 10, 10, 10, 10]
        self.lines_data = [None] * 14
        self.report = {}
        self.report['PRESS'] = {}
        self.report['DIGITAL'] = {}
        self.ST_flag = False
        self.init_press = 0

    def setupSignal(self):
        self.connect(self.action_exit, SIGNAL("triggered()"), self.actionExit)
        self.connect(self.action_config, SIGNAL("triggered()"), self.actionConfig)
        self.connect(self.action_start, SIGNAL("triggered()"), self.actionStart)
        self.connect(self.action_reset, SIGNAL("triggered()"), self.actionReset)
        self.connect(self.action_result, SIGNAL("triggered()"), self.actionResult)
        self.connect(self.action_print, SIGNAL("triggered()"), self.actionPrint)
        self.connect(self.action_back, SIGNAL("triggered()"), self.actionBack)
        self.connect(self.action_read_report, SIGNAL("triggered()"), self.actionReadReport)
        self.connect(self.notice_window.default_part.connect_button, SIGNAL("clicked()"), self.connectButtonClicked)
        self.connect(self.notice_window.default_part.read_file_button, SIGNAL("clicked()"), self.readFileButtonClicked)
        self.notice_window.current_press.ready_button.clicked.connect(self.readyButtonClicked)
        self.lcd_window.st_transfer.clicked.connect(self.setShiftTimeChange)
        #不能在外界直接操作GUI只能采用信号槽方式
        self.tcp_link.signal_tips.connect(self.notice_window.setLblNotice)
        self.tcp_link.signal_noticeText.connect(self.notice_window.setNoticeText)
        self.tcp_link.signal_progressBar.connect(self.notice_window.setValue)
        self.tcp_link.signal_lcd.connect(self.setPress6LCDValue)
        self.tcp_link.signal_trigger.connect(self.actionStart)
        self.tcp_link.signal_result.connect(self.connectResult)
        self.tcp_link.signal_timeout.connect(self.dataTimeout)
        #右侧LCD 显示
        self.curve_window.lcd_signal.connect(self.lcdDisplay)
        for i in self.chk_group:
            i.toggled.connect(self.lcdCheck)
        #数据收集阶段定时器，根据具体情况删减
        self.draw_timer = QTimer(self)
        self.connect(self.draw_timer,SIGNAL("timeout()"),self.waitDraw)

    def finishingLayout(self):
        self.left_layout = QVBoxLayout()
        self.right_layout = QHBoxLayout()
        self.notice_window = NoticeWidget(self)
        self.curve_window = CurveWidget(self)
        self.left_layout.addWidget(self.curve_window)
        self.left_layout.addWidget(self.notice_window)
        self.curve_window.hide()
        self.widget_container.setLayout(self.left_layout)
        self.explain_window = Explain(self)
        self.configuration_window = Configuration(self)
        self.lcd_window = LCDGroup(self)
        self.right_layout.addWidget(self.explain_window)
        self.right_layout.addWidget(self.configuration_window)
        self.right_layout.addWidget(self.lcd_window)
        self.configuration_window.hide()
        self.lcd_window.hide()
        self.frame_container.setLayout(self.right_layout)

    def setShow(self, flag):
        """flag must a int"""
        if flag == 1:
            self.curve_window.hide()
            self.notice_window.show()
            self.notice_window.update()
        elif flag == 2:
            #print self.notice_window.geometry()
            self.notice_window.hide()
            self.curve_window.show()
            self.curve_window.update()
            #print self.curve_window.geometry()
            #print self.widget_container.geometry()
        elif flag == 3:
            self.explain_window.show()
            self.explain_window.update()
            self.configuration_window.hide()
            self.lcd_window.hide()
        elif flag == 4:
            self.explain_window.hide()
            self.configuration_window.show()
            self.configuration_window.update()
            self.lcd_window.hide()
        elif flag == 5:
            self.explain_window.hide()
            self.configuration_window.hide()
            self.lcd_window.show()
            self.lcd_window.update()

    def setupAction(self, **kwargs):
        """
        kwargs = {"config":False,"start":False,"reset":False,"result":False,"print":False,"back":False,
                    "exit":False}
        """
        for i in kwargs.keys():
            self.__action[i] = kwargs[i]
        self.action_config.setEnabled(self.__action["config"])
        self.action_start.setEnabled(self.__action["start"])
        self.action_reset.setEnabled(self.__action["reset"])
        self.action_result.setEnabled(self.__action["result"])
        self.action_print.setEnabled(self.__action["printer"])
        self.action_back.setEnabled(self.__action["back"])
        self.action_exit.setEnabled(self.__action["exit"])

    def actionOrder(self, order):
        if order == 'init':
            self.setupAction(config=False, start=False, reset=False, result=False, printer=False, back=False)
            self.setShow(1)
            self.setShow(3)
            self.notice_window.setShow(1)
            self.notice_window.reset()
            self.notice_window.setLblNotice(u"点击[检测连接(Ctrl+Alt+L)]与下位机建立通信连接\
                                 \n点击[读取文档(Ctrl+Alt+R)]读取已保存的数据文档")
            self.action_back.setText(u"首页/断开")
        elif order =='config':
            self.setupAction(config=True, back=True)
            self.notice_window.setShow(2)
            self.setShow(1)
            self.setShow(4)
            self.notice_window.reset()
            self.notice_window.setLblNotice(u"点击[参数设置(F1)]对要进行测量的项目进行相关参数的设置\n"
                                 u"点击[断开连接(F7)]断开与下位机的通信")
            self.action_back.setText(u"断开连接")
        elif order == 'ready':
            self.setupAction(config=False, reset=True)
            self.setShow(1)
            self.setShow(4)
            self.notice_window.setShow(3)
            self.notice_window.setLblNotice(u"点击[准备测试(Ctrl+Alt+R)]进入测量\n"
                                            u"点击[复位(F3)]对配置信息进行重新配置")
        elif order == 'reset':
            self.setupAction(config=True, start=False,  reset=False, result=False, printer=False)
            self.notice_window.setShow(2)
            self.setShow(1)
            self.setShow(4)
            self.notice_window.setLblNotice(u"点击[参数设置(F1)]对要进行测量的项目进行相关参数的设置\
                                 \n点击[断开连接(F7)]断开与下位机的通信")
            self.notice_window.setNoticeText(u"对下次测试进行重新配置")
        elif order == 'trigger':
            self.notice_window.setShow(2)
            self.notice_window.setLblNotice(u'此时请勿进行其他操作，若要停止测试请点击[复位(F3)]')
            self.notice_window.setNoticeText(u'等待触发......')
        elif order == 'start':
            self.setupAction(start=True)
            self.notice_window.setShow(2)
            self.notice_window.setLblNotice(u'点击[开始(F2)]进行测量，若要重新测试请点击[复位(F3)]')
            self.notice_window.setNoticeText(u'手动触发方式')
        elif order == 'draw':
            self.setupAction(result=True, printer=True)
        elif order == 'tips':
            pass
        elif order == 'read':
            self.setShow(2)
            self.setShow(5)
            self.setupAction(back = True, result = True)
            self.action_back.setText(u"返回首页")

    def actionConfig(self):
        """根据配置对话框的内容获取相关参数"""
        config_dialog = ConfigDialog(self.tcp_link.getLineState)
        config_dialog.show()
        config_dialog.exec_()
        if config_dialog.getPassFlag():
            self.group_digital = [(i[0].text(), i[1].isChecked()) for i in config_dialog.group_digital]
            self.group_press = [(i[0].text(), i[1].isChecked(), i[2].currentIndex()) for i in config_dialog.group_press]
            self.group_speed_trigger = [config_dialog.speed_chk.isChecked(), config_dialog.trigger_combo.currentIndex()]
            #测试项目，项目名称，测试人员，测试日期
            self.groupNPTInfo = [config_dialog.testProject.currentIndex(), config_dialog.projectName_edit.text(),
                                 config_dialog.person_edit.text(), config_dialog.time_edit.text()]
            #测试时长
            self.measure_time = config_dialog.measureTime
            #测试距离
            self.measure_distance = config_dialog.measureDistance
            #set默认通道
            self.default_press = config_dialog.default_press.currentIndex()
            #设置默认膛压通道
            self.notice_window.setDefault(self.default_press)
            self.default_digital = config_dialog.default_digital.currentIndex()
            self.tcp_link.setPressChannel(self.default_press)
            self.tcp_link.setDigitalChannel(self.default_digital)
            self.tcp_link.setThresholdPress(config_dialog.threshold_press)
            self.tcp_link.setCalibration(config_dialog.calibration)
            self.tcp_link.setSpeedFactor(self.groupNPTInfo[0])
            #需要绘制的坐标系
            self.exist_axis = []
            #需要调整宽度的坐标系
            axis_num = []
            for i, j in enumerate(self.group_press):
                if j[1]:
                    self.exist_axis.append(i)
                    axis_num.append((i, j[2]))
                    self.scaleFactor[i] = self.scaleRegion[j[2]]
                    #if j[0]:
                        #self.report['PRESS'][i] = j[0]
                    #else:
                        #self.report['PRESS'][i] = u'通道%d' %(i + 1)
                else:
                    self.scaleFactor[i] = 0
                    #self.report['PRESS'][i] = None
            for i,j in enumerate(self.group_digital):
                if j[1]:
                    self.exist_axis.append(i+6)
                    #if j[0]:
                        #self.report['DIGITAL'][i] = j[0]
                    #else:
                        #self.report['DIGITAL'][i] = '通道%d' %(i + 1)
                #else:
                    #self.report['DIGITAL'][i] = None
            if self.group_speed_trigger[0]:
                self.exist_axis.extend([10, 11, 12])
                if self.groupNPTInfo[0] == 0:
                    axis_num.append((12, 1))
                else:
                    axis_num.append((12, 4))
            self.tcp_link.setFactor(self.scaleFactor[:])
            #print self.scaleFactor
            self.curve_window.produceAxis(self.exist_axis[:])
            for i in (axis_num):
                self.curve_window.setTicker(i[0], i[1])
            #开始根据配置获取需求值并显示当前压力
            self.tcp_link.setTestFlag(False)
            self.tcp_link.setCurrentFlag(True)
            #报告关键值
            #序列号
            self.report['SERIAL'] = self.groupNPTInfo[1]
            _test_type = [u'鱼雷',u'诱饵']
            self.report['TYPE'] =  _test_type[self.groupNPTInfo[0]]
            _trigger = [u'自动触发', u'手动触发', u'外触发']
            self.report['TRIGGER'] = _trigger[self.group_speed_trigger[1]] #触发方式
            self.report['PERSON'] = self.groupNPTInfo[2]  #测试人员
            self.report['DATE'] = self.groupNPTInfo[3]  #测试日期
            self.tcp_link.setCurrentFlag(True)
            self.actionOrder('ready')
            #print self.measure_distance
        self.configuration_window.readConfig()

    def actionStart(self):
        #print 'start'
        self.lcd_window.check([i[1] for i in self.group_press], [i[1] for i in self.group_digital],
                              self.group_speed_trigger[0])
        #print self.group_speed_trigger[0]
        self.tcp_link.setTriggerFlag(False)
        self.tcp_link.setClearFlag(False)
        self.setupAction(start=False)
        self.notice_window.reset()
        self.setShow(1)
        self.notice_window.setLblNotice(u'正在接收数据中，若想停止测量可直接点击[复位(F3)]终止本次测量')
        self.notice_window.setShow(2)
        self.notice_window.setNoticeText(u'系统正在测量，请等待......')
        self.notice_window.setValue(1)
        self.draw_count = 0
        self.draw_timer.start(100)
        self.draw_timer.setInterval(100)
    def waitDraw(self):
        self.draw_count += 0.1
        value = 100/(self.measure_time)*self.draw_count
        self.notice_window.setValue( value)
        if self.draw_count >= self.measure_time:
            self.draw()

    def draw(self):
        #关闭时间
        self.tcp_link.setClearFlag(True)
        self.draw_timer.stop()
        self.notice_window.setNoticeText(u'数据接收完毕，处理中......')


        data = self.tcp_link.getData()
        #若无数据直接返回
        if not data:
            self.actionReset()
            return
        #print len(data), 'total data'
        speed_data = data[15::16]
        self.handle = HandleData(speed_data, self.measure_distance)
        length = len(speed_data)
        #开始运动点num
        num = self.handle.getStartTime()
        shift = self.handle.shift()
        if self.groupNPTInfo[0] == 0:
            speed_out = self.handle.getOutTime(shift)
        else:
            speed_out = self.handle.getStopTime(shift, self.measure_distance)
        #所截取数据的长度
        right_limit = speed_out + 100
        if right_limit > length:
            right_limit = speed_out + 1
        if self.group_speed_trigger[0]:
            x_data = [(i - num) * 5E-4 for i in range(length)]
        else:
            x_data = [i * 5E-4 for i in range(length)]
        self.lines_data[0] = x_data[:right_limit]
        #print self.exist_axis
        for i in range(10):
            y_data = data[i::16]
            self.lines_data[i+1] = y_data[:right_limit]
            if i < 6:
                if i in self.exist_axis:
                    #不同测试类型取值不同
                    if self.groupNPTInfo[0] == 0:
                        _value = max(y_data)
                        self.report['PRESS'][i + 1] = '%0.2f' % _value
                        if i == self.default_press:
                            self.report['PRESS'][i + 1] = '%0.2f' % (_value - self.init_press)
                            self.handle.setChamberPressure(self.lines_data[i + 1], self.init_press)
                    else:
                        _value = y_data[speed_out]
                        self.report['PRESS'][i + 1] = '%0.2f' % _value
                    self.curve_window.drawLine2D(self.exist_axis.index(i), self.lines_data[0], self.lines_data[i+1],
                                                 self.color_sheet[i])
                else:
                     self.report['PRESS'][i + 1] = '--'
            else:
                if i in self.exist_axis:
                    begin = self.handle.bleedTime(y_data)
                    #dead = length - begin
                    #self.report['DIGITAL'][i - 5] = ('%0.2f' %(begin*5E-4), '%0.2f' %(dead*5E-4))
                    self.report['DIGITAL'][i - 5] = '%0.1f' % (begin*5E-4)
                    self.curve_window.drawLine2D(self.exist_axis.index(i), self.lines_data[0], self.lines_data[i+1],
                                                 self.color_sheet[i])
                else:
                    self.report['DIGITAL'][i - 5] = ('--')
        self.lines_data[11] = speed_data[:right_limit]
        #加速度
        acceleration = self.handle.acceleration()
        self.lines_data[12] = acceleration[:right_limit]
        self.lines_data[13] = shift[:right_limit]
        if 10 in self.exist_axis:
            self.report['SPEED'] = '%0.1f' % speed_data[speed_out]
            self.curve_window.drawLine2D(self.exist_axis.index(10), self.lines_data[0], self.lines_data[11],
                                         self.color_sheet[10])
            self.report['ACCELERATION'] = '%0.1f' %acceleration[speed_out]
            self.curve_window.drawLine2D(self.exist_axis.index(11), self.lines_data[0], self.lines_data[12],
                                         self.color_sheet[11])
            self.curve_window.drawLine2D(self.exist_axis.index(12), self.lines_data[0], self.lines_data[13],
                                         self.color_sheet[12])
        else:
            self.report['SPEED'] = '--'
            self.report['ACCELERATION'] = '--'
        #图像填充全屏
        self.curve_window.setXFull(self.lines_data[0][0], self.lines_data[0][-1])
        #延迟时间
        self.report['DELAY'] = '%0.1f' % (num * 5E-4)
        #发射时间
        self.report['SHOOT'] = '%0.1f' % (speed_out * 5E-4)
        #flag = self.report['DIGITAL'].get(self.default_digital + 1, ('--', '--'))
        if self.group_digital[self.default_digital][1]:
            begin, dead = self.handle.getStartClock(data[6 + self.default_digital::16])
            #print begin, dead
            #泄放阀开启时间
            self.report['OPEN'] = '%0.1f' % (begin*5E-4)
            #泄放阀开启时机
            self.report['BLEED'] = '%0.1f' % shift[dead]
        else:
            self.report['OPEN'] = '--'
            self.report['BLEED'] = '--'
        now_time = datetime.datetime.now()
        file_path = now_time.strftime("%Y%m%d%H%M%S")
        if self.groupNPTInfo[0] == 0:
            filename = u'鱼雷' + self.groupNPTInfo[1] + file_path
        else:
            filename = u'诱饵' + self.groupNPTInfo[1] + file_path
        #self.tempHTML(self.group_press, self.group_digital, './template/'+'image.png')
        self.tempPicture("./template/" + "image.png")
        self.saveReport('./report/'+filename+'.pdf')
        self.saveFile('./DigitalSheet/'+filename+'.csv')
        self.curve_window.updateDraw()
        self.curve_window._init_View()
        self.notice_window.setValue(100)
        self.setShow(2)
        self.setShow(5)
        self.actionOrder('draw')

    def tempPicture(self, filename):
        directory = os.path.dirname(filename)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        self.curve_window.canvas.print_figure(filename, dpi = 300)

    def saveReport(self, filename):
        directory = os.path.dirname(filename)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOrientation(QPrinter.Landscape)
        printer.setPageSize(QPrinter.A4)
        printer.setOutputFileName(filename)
        if filename:
            self.print_(printer)

    def print_(self, printer):
        painter = QPainter(printer)
        pageRect = printer.pageRect()
        w = pageRect.width() * 0.85
        h = pageRect.height()
        painter.drawPixmap(0, 0, w, h, './template/image.png')

        sansFont = QFont("Helvetica", 10)
        painter.setFont(sansFont)
        fm = QFontMetrics(sansFont)
        height = fm.height() + 10
        vmargin = 40

        x0 = w +1
        y = 25
        width = fm.width(u"测试编号") + 25
        x1 = x0 + width
        painter.drawText(x0, y, u"报告编号")
        painter.drawText(x1, y, self.report['SERIAL'])

        y += height
        painter.drawText(x0, y, u"测试类型")
        painter.drawText(x1, y, self.report['TYPE'])

        y += height
        painter.drawText(x0, y, u"触发方式")
        painter.drawText(x1, y, self.report['TRIGGER'])

        y += height
        painter.drawText(x0, y, u"测试人员")
        painter.drawText(x1, y, self.report['PERSON'])

        y += height
        painter.drawText(x0, y, u"测试日期")
        painter.drawText(x1, y, self.report['DATE'])


        y += vmargin
        width = fm.width(u"通道1") + 50
        x1 = x0 + width
        space = 0
        painter.drawText(x0 + 20, y, u"压力通道(Mpa)")
        for i, j in enumerate(self.group_press):
            if j[1]:
                y += height
                if j[0]:
                    painter.drawText(x0, y, j[0])
                else:
                    painter.drawText(x0, y, '通道%d'.decode("utf-8") %(i+1))
                painter.drawText(x1, y, self.report['PRESS'][i + 1])
            else:
                space += height


        y += (vmargin + space)
        width = fm.width(u"通道计量1") + 15
        x1 = x0 + width
        #x2 = x1 + width
        painter.drawText(x0 + 20, y, u"数字量计时通道(s)")
        y += height
        painter.drawText(x0, y, u"通道")
        painter.drawText(x1, y, u"开启时间")
        #painter.drawText(x2, y, u"关闭")
        space = 0
        for i, j in enumerate(self.group_digital):
            if j[1]:
                y += height
                if j[0]:
                    painter.drawText(x0, y, j[0])
                else:
                    painter.drawText(x0, y, '通道%d'.decode("utf-8") %(i+1))
                painter.drawText(x1, y, self.report['DIGITAL'][i + 1][0])
                #painter.drawText(x2, y, self.report['DIGITAL'][i + 1][1])
            else:
                space += height


        y += (vmargin + space)
        width = fm.width(u"出管速度(m/s)") + 25
        x1 = x0 + width
        painter.drawText(x0, y, u"加速度(g)")
        painter.drawText(x1, y, self.report['ACCELERATION'])

        y += height
        painter.drawText(x0, y, u"出管速度(m/s)")
        painter.drawText(x1, y, self.report['SPEED'])

        y += height
        painter.drawText(x0, y, u"延迟时间(s)")
        painter.drawText(x1, y, self.report['DELAY'])

        y += height
        painter.drawText(x0, y, u"发射时间(s)")
        painter.drawText(x1, y, self.report['SHOOT'])

        y += height
        painter.drawText(x0, y, u"发射深度(s)")
        painter.drawText(x1, y, self.report['DEEP'])

        width = fm.width(u"泄放装置泄放时间(s)") + 5
        y += height
        painter.drawText(x0, y, u"泄放阀开启时机(m)")
        x1 = x0 + width
        painter.drawText(x1, y, self.report['BLEED'])

        y += height
        painter.drawText(x0, y, u"泄放阀开启时间(s)")
        x1 = x0 + width + 1
        painter.drawText(x1, y, self.report['OPEN'])

    def saveFile(self, filename):
        directorys = os.path.dirname(filename)
        if not os.path.isdir(directorys):
            os.makedirs(directorys)
        if not os.path.isfile(filename):
            try:
                file = open(filename, 'w')
            except Exception, e:
                file.close()
                return
            press = '&'.join([self.report['PRESS'][i] for i in range(1, 7)])
            digital = '&'.join([self.report['DIGITAL'][i] for i in range(1, 5)])
            bleed_value = '&'.join([self.report['OPEN'], self.report['BLEED']])
            #20131216对保存的数据进行修改
            datapool = ['startest', self.report['SERIAL'], self.report['TYPE'], self.report['TRIGGER'],
                        self.report['PERSON'], self.report['DATE'], press, digital, self.report['ACCELERATION'],
                        self.report['SPEED'], self.report['DELAY'], self.report['SHOOT'], bleed_value, self.report['DEEP']]
            saveString = self.setText(','.join(datapool))
            #print saveString
            file.write(saveString)
            file.write('\n')
            datapool = []

            datapool.append('0')
            for i in range(6):
                datapool.append( '%d' %self.group_press[i][2])
            for i in range(4):
                datapool.append('0')
            datapool.append('0')
            datapool.append('0')
            if self.groupNPTInfo[0] == 0:
                datapool.append('1')
            else:
                datapool.append('4')
            saveString = ','.join(['%s' %i for i in datapool])
            file.write(saveString)
            file.write('\n')
            datapool = []

            datapool.append(True)
            datapool.extend([chk[1] for chk in self.group_press])
            datapool.extend([chk[1] for chk in self.group_digital])
            datapool.extend([self.group_speed_trigger[0] for i in range(3)])
            saveString = ','.join(['%s' %i for i in datapool])
            file.write(saveString)
            file.write('\n')
            datapool = []

            for i, j in enumerate(self.lines_data[0]):
                for k in range(14):
                    datapool.append(self.lines_data[k][i])
                saveString = ','.join(['%s' %v for v in datapool])
                file.write(saveString)
                file.write('\n')
                datapool = []
            file.close()

    def actionReset(self):
        if self.draw_timer.isActive():
            self.draw()
            return
        self.clear()
        self.tcp_link.sendReset()
        self.actionOrder('reset')

    def clear(self):
        #self.lines_data = [[]] * 14
        self.tcp_link.clear()
        self.tcp_link.setReadFlag(False)
        self.curve_window.clear()
        self.lcd_window.clear()
        for i in self.lcd_group:
            i.display('0')

    def actionResult(self):
        from ReportDialog import ReportDialog
        dialog = ReportDialog(self)
        dialog.setDisplay(self.report)
        dialog.setModal(True)
        dialog.show()
        dialog.exec_()

    def actionPrint(self):
        """打印报告"""
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.NativeFormat)
        printer.setOutputFileName("")
        printer.setOrientation(QPrinter.Landscape)
        printer.setPageSize(QPrinter.A4)
        #=======================================================#
        #无需选择
        printDialog = QPrintDialog(printer, self)
        #self.print_(printer)
        #如果需要选择打印机
        if printDialog.exec_():
            self.print_(printer)

    def actionBack(self):
        if self.draw_timer.isActive():
            ret = QMessageBox.warning(self, u"警告",u"测量正在进行中，是否中断测量" ,
                                      QMessageBox.Yes|QMessageBox.No)
            if ret == QMessageBox.No:
                return
            else:
                self.draw_timer.stop()
        self.clear()
        self.actionOrder('init')
        self.tcp_link.close()
        self.ST_flag = False

    def actionExit(self):
        self.close()

    def actionReadReport(self):
        if not os.path.isdir('./report'):
            os.mkdir('./report')
        filedialog = QFileDialog(self)
        files = filedialog.getOpenFileNames(self,
                                            u"读取报告", "report/",
                                            "PDF Files (*.pdf)")
        filename = files[0]
        if filename:
            import win32api
            win32api.ShellExecute(0, 'open', filename[0], '','',1)

    def connectButtonClicked(self):
        self.notice_window.setShow(2)
        self.notice_window.setLblNotice(u"正在与下位机建立通信中，请勿进行其他操作！")
        self.notice_window.setNoticeText(u"连接中，请稍等......")
        self.tcp_link.startConnect()

    def connectResult(self, flag):
        if flag[0]:
            result = flag[1]
            if False in result:
                self.tcp_link.sendTestResult(False)
                channel = []
                for i, j in enumerate(result):
                    if i < 6:
                        if not j:
                            channel.append(u'压力通道%s' %(i+1))
                    elif i < 10:
                        if not j:
                            channel.append(u'计时通道%s' %(i-5))
                    else:
                        if not j:
                            channel.append(u'速度通道')
                err = ','.join(channel)
                ret = QMessageBox.warning(self, u"警告",u"%s自检未通过，是否继续进行测量" %err ,
                                          QMessageBox.Yes|QMessageBox.No)
                if ret == QMessageBox.No:
                    self.failed()
                    return
            self.tcp_link.sendTestResult(True)
            self.notice_window.setNoticeText(u"设备运行正常，进行参数配置")
            self.notice_window.setValue(100)
            self.actionOrder("config")
        else:
            QMessageBox.warning(self, u'错误', u'请检查网线连接')
            self.failed()

    def failed(self):
        self.tcp_link.close()
        self.actionOrder('init')

    def getText(self, text):
        try:
            value = text.decode('utf-8')
        except:
            try:
                value = text.decode('gbk')
            except:
                try:
                    value = text.decode('gb2312')
                except:
                    value = ''
        return value

    def setText(self, text):
        try:
            value = text.encode('utf-8')
        except:
            try:
                value = text.encode('gbk')
            except:
                try:
                    value = text.encode('gb2312')
                except:
                    value = ''
        return value

    def readFileButtonClicked(self):
        if not os.path.isdir('./DigitalSheet'):
            os.mkdir('./DigitalSheet')
        filedialog = QFileDialog(self)
        files = filedialog.getOpenFileNames(self,
                                            u"读取文档", "DigitalSheet/",
                                            "excel Files (*.csv)")
        filename = files[0]
        if filename:
            try:
                file = open(filename[0], 'r')
                data = file.read().split('\n')[:-1]
                #关闭文件
                file.close()
                self.exist_axis = []
                axis_num = []
                interval = []
                check = []
                #提取第一行中的报告值
                _result = [i for i in data[0].split(",")]
                if _result[0] == 'startest':
                    for i, j in enumerate(['SERIAL', 'TYPE', 'TRIGGER', 'PERSON', 'DATE'], 1):
                        self.report[j] = _result[i]
                    self.report['TRIGGER'] = self.getText(self.report['TRIGGER'])
                    self.report['TYPE'] = self.getText(self.report['TYPE'])
                    for i, j in enumerate(_result[6].split('&'), 1):
                        self.report['PRESS'][i] = j
                    for i, j in enumerate(_result[7].split('&'), 1):
                        self.report['DIGITAL'][i] = j
                    self.report['ACCELERATION'] = _result[8]
                    self.report['SPEED'] = _result[9]
                    self.report['DELAY'] = _result[10]
                    self.report['SHOOT'] = _result[11]
                    self.report['OPEN'], self.report['BLEED'] = _result[12].split('&')
                    self.report['DEEP'] = _result[13]
                elif _result[0] == 'time':
                    for i in ['SERIAL', 'TYPE', 'TRIGGER', 'PERSON', 'DATE']:
                        self.report[i] = '**'
                    for i in range(1, 7):
                        self.report['PRESS'][i] = '**'
                    for i in range(1,5):
                        self.report['DIGITAL'][i] = '**'
                    for i in ['ACCELERATION', 'SPEED', 'DELAY', 'SHOOT', 'OPEN', 'BLEED', 'DEEP']:
                        self.report[i] = '**'

                #注意第一列为x轴
                for i in data[1].split(",")[1:]:
                    interval.append(int(i))
                for i, j in enumerate(data[2].split(',')[1:]):
                    if j == "True":
                        self.exist_axis.append(i)
                        axis_num.append((i, interval[i]))
                        check.append(True)
                    else:
                        check.append(False)
                #print check
                self.curve_window.produceAxis(self.exist_axis)
                for i in axis_num:
                    self.curve_window.setTicker(i[0], i[1])
                self.lcd_window.check(check[0:6], check[6:10], check[10])
                self.group_speed_trigger = [check[10]]
                #数据区域
                curve_data = ','.join(data[3:]).split(',')
                #todo 是否实数化
                #for i, j in enumerate(curve_data):
                #    curve_data[i] = float(j)
                for i in range(14):
                    self.lines_data[i] = curve_data[i::14]
                for i, j in enumerate(self.exist_axis):
                    self.curve_window.drawLine2D(i, self.lines_data[0], self.lines_data[j+1], self.color_sheet[j])
                self.curve_window.setXFull(float(self.lines_data[0][0]), float(self.lines_data[0][-1]))
                self.curve_window.updateDraw()
                self.curve_window._init_View()
                self.actionOrder("read")
                #print 'ok'
            except Exception, e:
                QMessageBox.critical(self,
                                    u"文档读取失败", u'文档格式有误或不存在\n'+str(e), QMessageBox.Ok, QMessageBox.NoButton)

    def readyButtonClicked(self):
        self.tcp_link.setCurrentFlag(False)
        self.init_press = self.notice_window.getLcdValue(self.default_digital)
        if self.group_press[self.default_press][1]:
            self.report['DEEP'] = '%0.f' % (self.init_press * 100)
        else:
            self.report['DEEP'] = '--'
        self.tcp_link.setInitPress(self.init_press)
        if self.group_speed_trigger[1] == 1:
            self.tcp_link.setTriggerFlag(False)
            self.actionOrder('start')
        else:
            self.actionOrder('trigger')
            if self.group_speed_trigger[1] == 0:
                self.tcp_link.setTriggerFlag(True)
            else:
                self.tcp_link.sendTigReady()
                #print 'start trigger'
                self.tcp_link.waitTrigger()
        self.tcp_link.setCurrentFlag(False)

    def setShiftTimeChange(self):
        if not self.group_speed_trigger[0]:
            QMessageBox.warning(self, u'错误', u'未对速度进行测量，无位移信息!')
            return
        self.ST_flag = not self.ST_flag
        if not self.curve_window.setShiftTimeChange(self.ST_flag):
            self.ST_flag = not self.ST_flag
            QMessageBox.warning(self, u'错误', u'未产生相对位移，无法进行转换')
        if self.ST_flag:
            self.lcd_window.shift_chk.setText(u"时间")
        else:
            self.lcd_window.shift_chk.setText(u"位移")

    def setPress6LCDValue(self, channel):
        """设置6个压力通道显示"""
        if self.group_press[channel[0]][1]:
            self.notice_window.setLcdValue(channel)
        else:
            self.notice_window.setLcdValue((channel[0], 0))

    def lcdCheck(self, checked):
        """
        lcd选择曲线的显示
        """
        sender = self.sender()
        for i, j in enumerate(self.chk_group):
            if sender == j and i in self.exist_axis:
                self.curve_window.setLinesDisplay(i, checked)
                break

    def lcdDisplay(self, args):
        """lcd显示"""
        index, value = args
        self.lcd_group[index].display(value)

    def dataTimeout(self):
        """当出现异常情况是的警告"""
        QMessageBox.warning(self, u"警告", u"请检查网线", QMessageBox.NoButton)
        self.actionBack()

    def closeEvent(self, event):
        ret = QMessageBox.question(self, u"警告", u"确定要关闭吗", QMessageBox.Yes|QMessageBox.No)
        if ret == QMessageBox.No:
            event.ignore()
            return
        self.tcp_link.close()

if __name__ == "__main__":
    from PySide.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    #window.setWindowFlags(window.windowFlags() &~ Qt.WindowMinMaxButtonsHint)
    window.setWindowFlags(window.windowFlags() &~ Qt.WindowMaximizeButtonHint)
    #window.setWindowFlags(Qt.FramelessWindowHint)
    window.show()
    sys.exit(app.exec_())

