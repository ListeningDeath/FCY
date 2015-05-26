# -*- coding: utf-8 -*-
from Ui_NoticeWidget import Ui_NoticeWidget
from PySide.QtGui import QWidget, QHBoxLayout, QApplication
from PySide.QtCore import Signal
from DefaultPart import DefaultPart
from ProgressRate import ProgressRate
from CurrentPress import CurrentPress


class NoticeWidget(Ui_NoticeWidget, QWidget):

    def __init__(self, parent=None):
        super(NoticeWidget, self).__init__(parent)
        self.setupUi(self)
        self.finishingLayout()

    def finishingLayout(self):
        """布局"""
        self.default_part = DefaultPart(self)
        self.progress_rate = ProgressRate(self)
        self.current_press = CurrentPress(self)
        self.central_layout = QHBoxLayout()
        self.central_layout.addWidget(self.default_part)
        self.central_layout.addWidget(self.progress_rate)
        self.central_layout.addWidget(self.current_press)
        self.wgt_content.setLayout(self.central_layout)
        self.progress_rate.hide()
        self.current_press.hide()

    def setShow(self, flag):
        """板块显示"""
        if flag == 1:
            self.default_part.show()
            self.default_part.updateGeometry()
            self.progress_rate.hide()
            self.current_press.hide()
        elif flag == 2:
            self.default_part.hide()
            self.progress_rate.show()
            self.progress_rate.updateGeometry()
            self.current_press.hide()
        elif flag == 3:
            self.default_part.hide()
            self.progress_rate.hide()
            self.current_press.show()
            self.current_press.updateGeometry()
        elif flag == 4:
            self.default_part.hide()
            self.progress_rate.hide()
            self.current_press.hide()

    def reset(self):
        self.progress_rate.reset()

    def setValue(self, value):
        self.progress_rate.setValue(value)

    def getValue(self):
        return self.progress_rate.value()

    def setNoticeText(self, text=""):
        self.progress_rate.setNoticeText(text)

    def setLblNotice(self, text=""):
        self.lbl_notice.setText(text)

    def setLcdValue(self, channel):
        #选择显示lcd值
        #print value
        index, value = channel
        self.current_press.display(index, "%6.3f" % value)

    def getLcdValue(self, index):
        return self.current_press.getLcdValue(index)

    def setDefault(self, index):
        self.current_press.setDefault(index)

if __name__ == "__main__":
    from PySide.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    window = NoticeWidget()
    window.show()
    sys.exit(app.exec_())
