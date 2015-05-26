# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_designer\NoticeWidget.ui'
#
# Created: Tue Oct 29 11:07:30 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NoticeWidget(object):
    def setupUi(self, NoticeWidget):
        NoticeWidget.setObjectName("NoticeWidget")
        NoticeWidget.resize(754, 506)
        NoticeWidget.setStyleSheet("QLabel{\n"
"font-family:\"Arial\";\n"
"}")
        self.verticalLayout_2 = QtGui.QVBoxLayout(NoticeWidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QtGui.QFrame(NoticeWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(160, 160))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/toolbar/tishi.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.frame = QtGui.QFrame(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.lbl_notice = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_notice.sizePolicy().hasHeightForWidth())
        self.lbl_notice.setSizePolicy(sizePolicy)
        self.lbl_notice.setStyleSheet("QLabel#lbl_notice{\n"
"font-size:15pt;\n"
"font-family:\"Arial\";\n"
"}")
        self.lbl_notice.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_notice.setWordWrap(True)
        self.lbl_notice.setObjectName("lbl_notice")
        self.verticalLayout.addWidget(self.lbl_notice)
        self.horizontalLayout.addWidget(self.frame)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.wgt_content = QtGui.QWidget(NoticeWidget)
        self.wgt_content.setObjectName("wgt_content")
        self.verticalLayout_2.addWidget(self.wgt_content)

        self.retranslateUi(NoticeWidget)
        QtCore.QMetaObject.connectSlotsByName(NoticeWidget)

    def retranslateUi(self, NoticeWidget):
        NoticeWidget.setWindowTitle(QtGui.QApplication.translate("NoticeWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NoticeWidget", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">提示:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_notice.setText(QtGui.QApplication.translate("NoticeWidget", "点击[检测连接(Ctrl+Alt+L)]与下位机建立通信连接\n"
"点击[读取文档(Ctrl+Alt+R)]读取已测过数据", None, QtGui.QApplication.UnicodeUTF8))

import Icons_rc
