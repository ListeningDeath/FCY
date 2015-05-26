# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_designer\ProgressRate.ui'
#
# Created: Fri Jul 19 09:09:34 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ProgressRate(object):
    def setupUi(self, ProgressRate):
        ProgressRate.setObjectName("ProgressRate")
        ProgressRate.setWindowModality(QtCore.Qt.NonModal)
        ProgressRate.resize(702, 208)
        ProgressRate.setWindowTitle("")
        self.verticalLayout = QtGui.QVBoxLayout(ProgressRate)
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_notice = QtGui.QLabel(ProgressRate)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_notice.sizePolicy().hasHeightForWidth())
        self.lbl_notice.setSizePolicy(sizePolicy)
        self.lbl_notice.setStyleSheet("font-size:14pt; \n"
"font-weight:600;")
        self.lbl_notice.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_notice.setObjectName("lbl_notice")
        self.verticalLayout.addWidget(self.lbl_notice)
        self.progressBar = QtGui.QProgressBar(ProgressRate)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(ProgressRate)
        QtCore.QMetaObject.connectSlotsByName(ProgressRate)

    def retranslateUi(self, ProgressRate):
        self.lbl_notice.setText(QtGui.QApplication.translate("ProgressRate", "在测试中，数据读取中，请稍等", None, QtGui.QApplication.UnicodeUTF8))

import Icons_rc
