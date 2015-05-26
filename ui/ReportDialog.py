# -*- coding: utf-8 -*-
from Ui_ReportDialog import Ui_ReportDialog
from PySide.QtGui import QDialog


class ReportDialog(QDialog, Ui_ReportDialog):
    def __init__(self, parent=None):
        super(ReportDialog, self).__init__(parent)
        self.setupUi(self)
        self.press = [self.press_ch1, self.press_ch2, self.press_ch3, self.press_ch4, self.press_ch5, self.press_ch6]
        self.digital = [self.digital_open_ch1, self.digital_open_ch2, self.digital_open_ch3, self.digital_open_ch4]

    def setDisplay(self, reportdata):
        for i in range(6):
            self.press[i].setText(reportdata['PRESS'][i + 1])
        for i in range(4):
            self.digital[i].setText(reportdata['DIGITAL'][i + 1])
        self.speed.setText(reportdata['SPEED'])
        self.acceleration.setText(reportdata['ACCELERATION'])
        self.shoot_deep.setText(reportdata['DEEP'])
        self.trigger_method.setText(reportdata['TRIGGER'])
        self.test_program.setText(reportdata['TYPE'])
        self.delay_time.setText(reportdata['DELAY'])
        self.shoot_time.setText(reportdata['SHOOT'])
        self.bleed_time.setText(reportdata['BLEED'])
        self.bleed_open_time.setText(reportdata['OPEN'])
