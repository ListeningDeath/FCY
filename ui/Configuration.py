# -*- coding:utf8
from PySide.QtGui import QWidget
from Ui_Configuration import Ui_Configuration
from ConfigParser import ConfigParser


class Configuration(QWidget, Ui_Configuration):
    def __init__(self, parent=None):
        super(Configuration, self).__init__(parent)
        self.setupUi(self)
        self.readConfig()

    def initUI(self):
        for i in [self.dswitch_lbl1, self.dswitch_lbl2, self.dswitch_lbl3, self.dswitch_lbl4]:
            i.setText(u"关闭")
        for i in [self.pswitch_lbl1, self.pswitch_lbl2, self.pswitch_lbl3, self.pswitch_lbl4, self.pswitch_lbl5,
                  self.pswitch_lbl6]:
            i.setText(u"关闭")
        for i in [self.prange_lbl1, self.prange_lbl2, self.prange_lbl3, self.prange_lbl4, self.prange_lbl5,
                  self.prange_lbl6]:
            i.setText("10Mpa")
        self.spswitch_lbl.setText(u"关闭")
        self.trigger_lbl.setText(u"自动触发")
        self.time_lbl.setText("10s")
        self.distance_lbl.setText("0.48m")

    def readConfig(self):
        try:
            self.loadConfig('conf/temp.ini')
        except:
            pass

    def loadConfig(self, filename):
        config = ConfigParser()
        if filename:
            config.read(filename)
            for i, j in enumerate([self.dswitch_lbl1, self.dswitch_lbl2, self.dswitch_lbl3, self.dswitch_lbl4]):
                section = "DIGITAL%d" % i
                checkable = config.getint(section, 'checkable')
                if checkable == 1:
                    j.setText(u"开启")
                else:
                    j.setText(u"关闭")
            temp_press = ["25Mpa", "10Mpa", "5Mpa", "2Mpa", "1Mpa"]
            for i, j in enumerate([(self.pswitch_lbl1, self.prange_lbl1), (self.pswitch_lbl2, self.prange_lbl2),
                                   (self.pswitch_lbl3, self.prange_lbl3), (self.pswitch_lbl4, self.prange_lbl4),
                                   (self.pswitch_lbl5, self.prange_lbl5), (self.pswitch_lbl6, self.prange_lbl6)]):
                section = "PRESSURE%d" % i
                checkable = config.getint(section, 'checkable')
                if checkable == 1:
                    j[0].setText(u"开启")
                else:
                    j[0].setText(u"关闭")
                j[1].setText(temp_press[config.getint(section, 'value')])

            if config.getint('SPEED', 'speed') == 1:
                self.spswitch_lbl.setText(u"开启")
            else:
                self.spswitch_lbl.setText(u"关闭")

            temp_trigger = [u"自动触发", u"手动触发", u"外触发"]
            self.trigger_lbl.setText(temp_trigger[config.getint('SPEED', 'pattern')])
            self.time_lbl.setText("%ss" % config.getint('PARAMETERS', 'timer'))
            yulei = config.getfloat('PARAMETERS', 'yulei')
            youer = config.getfloat('PARAMETERS', 'youer')
            test_project = config.getint('PARAMETERS', 'progect')
            if test_project == 0:
                self.distance_lbl.setText("%sm" % yulei)
            else:
                self.distance_lbl.setText("%sm" % youer)




if __name__ == "__main__":
    from PySide.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    window = Configuration()
    window.readConfig()
    window.show()
    sys.exit(app.exec_())

