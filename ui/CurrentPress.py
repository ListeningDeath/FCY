# -*- coding: utf-8 -*-
from PySide.QtGui import QWidget
from Ui_CurrentPress import Ui_CurrentPress


class CurrentPress(QWidget, Ui_CurrentPress):
    def __init__(self, parent=None):
        super(CurrentPress, self).__init__(parent)
        self.setupUi(self)
        self.lcd_group = [self.press_lcd1, self.press_lcd2, self.press_lcd3, self.press_lcd4, self.press_lcd5,
                          self.press_lcd6]

    #def display(self, value):
        #self.press_lcd.display(value)

    def display(self, index, value):
        """选择lcd显示"""
        self.lcd_group[index].display(value)

    def getLcdValue(self, index):
        return self.lcd_group[index].value()

    def setDefault(self, index):
        for i in self.lcd_group:
            i.setStyleSheet(u"")
        self.lcd_group[index].setStyleSheet(u"QLCDNumber{background-color:yellow;}")

if __name__ == "__main__":
    import sys
    from PySide.QtGui import QApplication
    app = QApplication(sys.argv)
    window = CurrentPress()
    window.show()
    sys.exit(app.exec_())
