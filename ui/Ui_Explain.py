# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_designer\Explain.ui'
#
# Created: Mon Sep 23 16:23:12 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Explain(object):
    def setupUi(self, Explain):
        Explain.setObjectName("Explain")
        Explain.resize(171, 553)
        self.verticalLayout = QtGui.QVBoxLayout(Explain)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(Explain)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/image/info.png"))
        self.label.setScaledContents(True)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi(Explain)
        QtCore.QMetaObject.connectSlotsByName(Explain)

    def retranslateUi(self, Explain):
        Explain.setWindowTitle(QtGui.QApplication.translate("Explain", "Form", None, QtGui.QApplication.UnicodeUTF8))

import Icons_rc
