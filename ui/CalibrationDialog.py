# -*- coding: utf-8 -*-
from PySide import QtGui
from Ui_CalibrationDialog import Ui_CalibrationDialog


class CalibrationDialog(QtGui.QDialog, Ui_CalibrationDialog):
    def __init__(self, parent = None):
        super(CalibrationDialog, self).__init__(parent)
        self.setupUi(self)
        self.setModal(True)
        self.spin_group = [self.press_spin1, self.press_spin2, self.press_spin3,
                           self.press_spin4, self.press_spin5, self.press_spin6]
        self.correct_flag = False
        self.ok_button.clicked.connect(self.ok_buttonClick)
        #self.cancel_button.clicked.connect(self.cancel_buttonClick)

    def getSpinGroupValue(self):
        return [i.value() for i in self.spin_group]

    def setSpinGroupValue(self, value):
        for i, j in enumerate(self.spin_group):
            j.setValue(value[i])

    def ok_buttonClick(self):
        self.correct_flag = True
        self.accept()

