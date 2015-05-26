# -*- coding: utf-8 -*-
from PySide.QtGui import QWidget
from Ui_ProgressRate import Ui_ProgressRate


class ProgressRate(QWidget, Ui_ProgressRate):
    def __init__(self, parent=None):
        super(ProgressRate, self).__init__(parent)
        self.setupUi(self)
        self.progressBar.reset()

    def reset(self):
        """重置"""
        self.progressBar.reset()

    def setNoticeText(self, text=""):
        """设置提示语"""
        if isinstance(text, str) or isinstance(text, unicode):
            self.lbl_notice.setText(text)
        else:
            self.lbl_notice.setText("")

    def setValue(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            self.progressBar.hide()
        else:
            self.progressBar.show()

    def value(self):
        return self.progressBar.value()

if __name__ == "__main__":
    import sys
    from PySide.QtGui import QApplication
    app = QApplication(sys.argv)
    window = ProgressRate()
    window.show()
    sys.exit(app.exec_())

