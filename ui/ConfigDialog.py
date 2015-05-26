# -*- coding: utf-8 -*-
from Ui_ConfigDialog import Ui_ConfigDialog
from Ui_DialogMatch import Ui_DialogMatch
from PySide.QtGui import QDialog, QMessageBox, QFileDialog, QPalette
from PySide.QtCore import QDateTime, Qt
from ConfigParser import ConfigParser
from CalibrationDialog import CalibrationDialog
import os


class ConfigDialog(QDialog, Ui_ConfigDialog):
    def __init__(self, line_state, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(600, 480)
        self.line_state = line_state
        self.measureTime = 10
        self.yulei = 7
        self.youer = 0.48
        self.measureDistance = self.yulei
        self.threshold_press = 0.05
        #压力校准值
        self.calibration = [-0.1013, -0.1013, -0.1013, -0.1013, -0.1013, -0.1013]
        #本次配置有效否
        self.passFlag = False
        self.testdate = QDateTime.currentDateTime().toString('yyyy-MM-dd')
        self.setupSignal()
        #设置相关标志属性
        self.setupGroup()
        self.time_edit.setText(self.testdate)
        self.time_edit.setReadOnly(True)
        self.defaultConfig(True)
        self.projectName_edit.setText("")

    def defaultConfig(self, flag):
        """
        flag 为true时load否则为save
        """
        if not os.path.isdir('conf'):
            os.mkdir('conf')
        if flag:
            try:
                self.loadConfig('conf/temp.ini')
            except Exception, e:
                #todo 是否为用户添加提示信息？
                #print str(e)
                self.setMeasureDistance(self.yulei)
                self.defaultConfig(False)
        else:
            try:
                file = open('conf/temp.ini', 'w')
                self.saveConfig(file)
            except Exception, e:
                #print str(e)
                pass
            finally:
                file.close()

    def setupSignal(self):
        #button
        self.testProject.currentIndexChanged.connect(self.projectChanged)
        self.testTimer.editingFinished.connect(self.timerChanged)
        self.loadConfigButton.clicked.connect(self.loadConfigButtonClicked)
        self.saveConfigButton.clicked.connect(self.saveConfigButtonClicked)
        self.matchButton.clicked.connect(self.matchButtonClicked)
        self.clearButton.clicked.connect(self.clear)
        self.projectName_edit.editingFinished.connect(self.nameCheck)
        self.test_shift.valueChanged.connect(self.setMeasureDistance)
        self.calibrationButton.clicked.connect(self.setCalibration)
        #self.default_press.currentIndexChanged.connect(self.setDefaultPress)
        #self.default_digital.currentIndexChanged.connect(self.setDefaultDigital)

    def setMeasureDistance(self, value):
        self.measureDistance = float(value)
        if self.testProject.currentIndex() == 0:
            self.yulei = self.measureDistance
        else:
            self.youer = self.measureDistance

    def setDefaultDigital(self):
        if self.default_digital.currentIndex() == 0:
            QMessageBox.warning(self, u"警告", u"通道1不能用于泄放阀计量")
            self.default_digital.setCurrentIndex(1)

    def nameCheck(self):
        text = self.projectName_edit.text()
        if text:
            try:
                f = open(text, 'w')
                f.close()
            except:
                QMessageBox.warning(self, u"错误", u"报告编号中不能输入非法字符")
                self.projectName_edit.setText("")
        if os.path.isfile(text):
            os.remove(text)

    def projectChanged(self, index):
        if index == 0:
            self.test_shift.setValue(self.yulei)
            self.speed_chk.setEnabled(True)
        elif index == 1:
            self.speed_chk.setEnabled(False)
            self.speed_chk.setCheckState(Qt.Checked)
            self.test_shift.setValue(self.youer)

    def timerChanged(self):
        if self.testTimer.value() <= 30:
            self.measureTime = self.testTimer.value()
        else:
            QMessageBox.information(self,u'输入错误', u'测量时间必须在5-30s之间，请输入正确时间值')
            self.testTimer.setValue(10)

    def setupGroup(self):
        #数字量
        self.group_digital = [[self.num_edit1, self.num_chk1], [self.num_edit2, self.num_chk2],
                              [self.num_edit3, self.num_chk3], [self.num_edit4, self.num_chk4]]
        #压力
        self.group_press = [[self.pres_edit1, self.pres_chk1, self.pres_combo1],
                            [self.pres_edit2, self.pres_chk2, self.pres_combo2],
                            [self.pres_edit3, self.pres_chk3, self.pres_combo3],
                            [self.pres_edit4, self.pres_chk4, self.pres_combo4],
                            [self.pres_edit5, self.pres_chk5, self.pres_combo5],
                            [self.pres_edit6, self.pres_chk6, self.pres_combo6]]

    def loadConfigButtonClicked(self):
        """
        load the config
        """
        if not os.path.isdir('conf'):
            os.mkdir('conf')
        files = QFileDialog.getOpenFileName(self,
                                            u"读取配置文件",
                                            "conf/default.ini",
                                            "INI File (*.ini)",
                                            )
        filename = files[0]
        try:
            self.loadConfig(filename)
        except Exception, e:
            QMessageBox.information(self, u'读取失败', u'配置文档有误，请重新配置'+str(e))

    def loadConfig(self, filename):
        config = ConfigParser()
        if filename:
            config.read(filename)
            for i in range(len(self.group_digital)):
                section = "DIGITAL%d" % i
                self.group_digital[i][0].setText(config.get(section, 'name').decode('utf-8'))
                checkable = config.getint(section, 'checkable')
                if checkable == 1:
                    self.group_digital[i][1].setCheckState(Qt.Checked)
                else:
                    self.group_digital[i][1].setCheckState(Qt.Unchecked)
            for i in range(len(self.group_press)):
                section = "PRESSURE%d" % i
                self.group_press[i][0].setText(config.get(section, 'name').decode('utf-8'))
                checkable = config.getint(section, 'checkable')
                if checkable == 1:
                    self.group_press[i][1].setCheckState(Qt.Checked)
                else:
                    self.group_press[i][1].setCheckState(Qt.Unchecked)
                self.group_press[i][2].setCurrentIndex(config.getint(section, 'value'))

            if config.getint('SPEED', 'speed') == 1:
                self.speed_chk.setCheckState(Qt.Checked)
            else:
                self.speed_chk.setCheckState(Qt.Unchecked)

            self.trigger_combo.setCurrentIndex(config.getint('SPEED', 'pattern'))

            self.projectName_edit.setText(config.get('LOG', 'project').decode('utf-8'))
            self.person_edit.setText(config.get('LOG', 'person').decode('utf-8'))
            #parameters
            self.testProject.setCurrentIndex(config.getint('PARAMETERS', 'progect'))
            self.testTimer.setValue(config.getfloat('PARAMETERS', 'timer'))
            self.yulei = config.getfloat('PARAMETERS', 'yulei')
            self.youer = config.getfloat('PARAMETERS', 'youer')
            self.default_digital.setCurrentIndex(config.getint('PARAMETERS', 'default_digital'))
            self.default_press.setCurrentIndex(config.getint('PARAMETERS', 'default_press'))
            self.threshold_press = config.getfloat('PARAMETERS', 'threshold_press')
            for i, j in enumerate(['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6']):
                self.calibration[i] = config.getfloat('CALIBRATION', j)
                #print self.calibration
            if self.testProject.currentIndex() == 0:
                self.measureDistance = self.yulei
            else:
                self.measureDistance = self.youer
            self.test_shift.setValue(self.measureDistance)
            self.measureTime = self.testTimer.value()

    def saveConfigButtonClicked(self):
        """
        save the config to conf/default.ini
        """
        ret = QMessageBox.warning(self, u"警告", u"确定要保存吗", QMessageBox.Yes|QMessageBox.No)
        if ret == QMessageBox.No:
            return
        if not os.path.isdir('conf'):
            os.mkdir('conf')
        files = QFileDialog.getSaveFileName(self,
                                            u"保存配置文件",
                                            "conf/default.ini",
                                            "INI File (*.ini)", )
        filename = files[0]
        if filename:
            try:
                file = open(filename, 'w')
                self.saveConfig(file)
            except Exception, e:
                QMessageBox.information(self, u'保存失败', u'文件选择错误'+str(e))
                return
            finally:
                file.close()

    def saveConfig(self, file):
        """
        保存配置文件
        """
        filename = file.name
        config = ConfigParser()
        if filename:
            config.read(file.name)
            #digital
            for i in range(len(self.group_digital)):
                section = "DIGITAL%d" % i
                config.add_section(section)
                if self.group_digital[i][1].isChecked():
                    config.set(section, 'name', self.group_digital[i][0].text().encode('utf-8'))
                    config.set(section, 'checkable', 1)
                else:
                    config.set(section, 'name', '')
                    config.set(section, 'checkable', 0)
                    #press
            for i in range(len(self.group_press)):
                section = "PRESSURE%d" %i
                config.add_section(section)
                if self.group_press[i][1].isChecked():
                    config.set(section, 'name', self.group_press[i][0].text().encode('utf-8'))
                    config.set(section, 'checkable', 1)
                    config.set(section, 'value', self.group_press[i][2].currentIndex())
                else:
                    config.set(section, 'name', '')
                    config.set(section, 'checkable', 0)
                    config.set(section, 'value', 1)
                    #speed
            section = "SPEED"
            config.add_section(section)
            if self.speed_chk.isChecked():
                config.set(section, 'speed', 1)
            else:
                config.set(section, 'speed', 0)
            config.set(section, 'pattern', self.trigger_combo.currentIndex())
            #print self.trigger_combo.currentIndex()
            #logs
            section = "LOG"
            config.add_section(section)
            config.set(section, 'person', self.person_edit.text().encode('utf-8'))
            config.set(section, 'project', self.projectName_edit.text().encode('utf-8'))
            config.set(section, 'datetime', self.time_edit.text().encode('utf-8'))
            #parameters
            section = "PARAMETERS"
            config.add_section(section)
            config.set(section, 'yulei', self.yulei)
            config.set(section, 'youer', self.youer)
            config.set(section, 'default_digital', self.default_digital.currentIndex())
            config.set(section, 'default_press', self.default_press.currentIndex())
            config.set(section, 'threshold_press', self.threshold_press)
            config.set(section, 'progect', self.testProject.currentIndex())
            config.set(section, 'timer', self.testTimer.value())
            section = "CALIBRATION"
            config.add_section(section)
            for i, j in enumerate(['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6']):
                config.set(section, j, self.calibration[i])
            config.write(file)
            #匹配连接线路

    def matchButtonClicked(self):
        """
        press:1--6;digital 1 - 4 ;速度；外触发
        """
        result = self.line_state()
        #print result
        if result == 'N/A' or len(result) != 12:
            result = '111111111111'
        self.matchResult(result)
        #self.passFlag = True

    def clear(self):
        for i in self.group_digital:
            i[0].setText('')
            i[1].setCheckState(Qt.Unchecked)
        for i in self.group_press:
            i[0].setText('')
            i[1].setCheckState(Qt.Unchecked)
            i[2].setCurrentIndex(1)
        self.speed_chk.setCheckState(Qt.Unchecked)
        self.trigger_combo.setCurrentIndex(0)
        self.projectName_edit.setText('')
        self.person_edit.setText('')
        self.time_edit.setText(self.testdate)
        self.testProject.setCurrentIndex(0)
        self.testTimer.setValue(10)
        self.default_press.setCurrentIndex(0)
        self.default_digital.setCurrentIndex(0)

    def setCalibration(self):
        dialog = CalibrationDialog(self)
        dialog.setSpinGroupValue(self.calibration)
        dialog.setSpinGroupValue(self.calibration)
        dialog.show()
        dialog.exec_()
        if not  dialog.correct_flag:
            return
        self.calibration = dialog.getSpinGroupValue()
        #print self.calibration
        config = ConfigParser()
        try:
            file = open("./conf/temp.ini", 'a+')
            config.read(file.name)
            section = "CALIBRATION"
            if not config.has_section(section):
                config.add_section(section)
            for i, j in enumerate(['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6']):
                config.set(section, j, self.calibration[i])
            config.write(file)
        except Exception, e:
            QMessageBox.information(self, u'读取失败', u'配置文档有误，请重新配置'+str(e))
        finally:
            file.close()

    def getPassFlag(self):
        return self.passFlag

    def getCalibration(self):
        return self.calibration

    def matchResult(self, result):
        """
        显示匹配状态
        """
        isMatch = True
        match_num = 0

        def accept():
            if isMatch:
                self.passFlag = True
                dialog.accept()
                self.defaultConfig(False)
                self.close()
            else:
                self.passFlag = False
                dialog.reject()
        dialog = QDialog()
        ui = Ui_DialogMatch()
        ui.setupUi(dialog)
        ui.okButton.clicked.connect(accept)
        dialog.setModal(True)
        groupState = [ui.pressure1, ui.pressure2, ui.pressure3, ui.pressure4, ui.pressure5, ui.pressure6,
                      ui.digital1, ui.digital2, ui.digital3, ui.digital4, ui.speed1, ui.speed2]
        groupCheck = [self.pres_chk1, self.pres_chk2, self.pres_chk3, self.pres_chk4, self.pres_chk5, self.pres_chk6,
                      self.num_chk1, self.num_chk2, self.num_chk3, self.num_chk4, self.speed_chk]
        if not result:
            return
        else:
            for i, j in enumerate(result):
                if i < 11:
                    if result[i] == '0':
                        if groupCheck[i].isChecked():
                            groupState[i].setText(u'匹配')
                            palette = groupState[i].palette()
                            palette.setColor(QPalette.WindowText,Qt.green)
                            groupState[i].setPalette(palette)
                            match_num += 1
                        else:
                            groupState[i].setText(u'接通')
                            palette = groupState[i].palette()
                            palette.setColor(QPalette.WindowText, Qt.blue)
                            groupState[i].setPalette(palette)
                    else:
                        if groupCheck[i].isChecked():
                            groupState[i].setText(u'不匹配')
                            palette = groupState[i].palette()
                            palette.setColor(QPalette.WindowText, Qt.red)
                            groupState[i].setPalette(palette)
                            ui.okButton.setEnabled(False)
                            isMatch = False
                        else:
                            groupState[i].setText(u'断开')
                            palette = groupState[i].palette()
                            palette.setColor(QPalette.WindowText, Qt.gray)
                            groupState[i].setPalette(palette)
                else:
                    if result[i] == '0':
                        self.trigger_combo.setCurrentIndex(2)
                        groupState[i].setText(u'外触发启用')
                        palette = groupState[i].palette()
                        palette.setColor(QPalette.WindowText, Qt.green)
                        groupState[i].setPalette(palette)
                        match_num += 1
                    else:
                        if self.trigger_combo.currentIndex() == 2:
                            groupState[i].setText(u'不匹配')
                            palette = groupState[i].palette()
                            palette.setColor(QPalette.WindowText, Qt.red)
                            groupState[i].setPalette(palette)
                            ui.okButton.setEnabled(False)
                            isMatch = False
                        else:
                            groupState[i].setText(u'断开')
                            palette = groupState[i].palette()
                            palette.setColor(QPalette.WindowText, Qt.gray)
                            groupState[i].setPalette(palette)
            if isMatch:
                ui.linkState.setText(u'匹配成功，%d条线路匹配' %match_num)
            else:
                ui.linkState.setText(u'匹配失败，%d条线路匹配' %match_num)
            dialog.show()
            dialog.exec_()

    def closeEvent(self, *args, **kwargs):
        pass

if __name__ == "__main__":
    from PySide.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    window = ConfigDialog(1)
    window.show()
    sys.exit(app.exec_())
