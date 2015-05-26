from PySide.QtGui import QWidget
from PySide.QtCore import Qt
from Ui_LCDGroup import Ui_LCDGroup


class LCDGroup(QWidget, Ui_LCDGroup):
    def __init__(self, parent=None):
        super(LCDGroup, self).__init__(parent)
        self.setupUi(self)
        self.presses = [self.press_chk1, self.press_chk2, self.press_chk3, self.press_chk4,
                        self.press_chk5, self.press_chk6]
        self.digitals = [self.digital_chk1, self.digital_chk2, self.digital_chk3, self.digital_chk4]

    def clear(self):
        for i in self.presses:
            i.setCheckState(Qt.Unchecked)
        for i in self.digitals:
            i.setCheckState(Qt.Unchecked)
        for i in [self.speed_chk, self.acceleration_chk, self.shift_chk]:
            i.setCheckState(Qt.Unchecked)

    def check(self, group_press, group_digital, speed):
        for i, j in enumerate(group_press):
            if j:
                self.presses[i].setEnabled(True)
                self.presses[i].setCheckState(Qt.Checked)
            else:
                self.presses[i].setCheckState(Qt.Unchecked)
                self.presses[i].setEnabled(False)
        for i, j in enumerate(group_digital):
            if j:
                self.digitals[i].setEnabled(True)
                self.digitals[i].setCheckState(Qt.Checked)
            else:
                self.digitals[i].setCheckState(Qt.Unchecked)
                self.digitals[i].setEnabled(False)
        if speed:
            self.speed_chk.setCheckState(Qt.Checked)
            self.speed_chk.setEnabled(True)
            self.acceleration_chk.setCheckState(Qt.Checked)
            self.acceleration_chk.setEnabled(True)
            self.shift_chk.setCheckState(Qt.Checked)
            self.shift_chk.setEnabled(True)
        else:
            self.speed_chk.setCheckState(Qt.Unchecked)
            self.speed_chk.setEnabled(False)
            self.acceleration_chk.setCheckState(Qt.Unchecked)
            self.acceleration_chk.setEnabled(False)
            self.shift_chk.setCheckState(Qt.Unchecked)
            self.shift_chk.setEnabled(False)



if __name__ == "__main__":
    from PySide.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    window = LCDGroup()
    window.show()
    sys.exit(app.exec_())
