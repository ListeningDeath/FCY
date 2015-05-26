# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_designer\DefaultPart.ui'
#
# Created: Tue Oct 29 11:06:04 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DefaultPart(object):
    def setupUi(self, DefaultPart):
        DefaultPart.setObjectName("DefaultPart")
        DefaultPart.resize(572, 218)
        self.gridLayout = QtGui.QGridLayout(DefaultPart)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(94, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.connect_button = QtGui.QPushButton(DefaultPart)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connect_button.sizePolicy().hasHeightForWidth())
        self.connect_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.connect_button.setFont(font)
        self.connect_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.connect_button.setStyleSheet("QPushButton#connect_button {\n"
"    font: 20pt \"Arial\";\n"
"    background:qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.05                     #77d42a, stop:1 #5cb811);\n"
"    border-style:outset;\n"
"    border-width:2px;\n"
"    border-radius:12px;\n"
"    border-color:#636363;\n"
"    padding:9px 18px \n"
"}\n"
"\n"
"QPushButton#connect_button:hover{\n"
"    background:qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.05                     #5cb811, stop:1 #77d42a);\n"
"}\n"
"\n"
"QPushButton#connect_button:pressed {\n"
"     background: #adff2f;\n"
"     border-style: inset;}\n"
"")
        self.connect_button.setIconSize(QtCore.QSize(48, 48))
        self.connect_button.setAutoRepeat(False)
        self.connect_button.setDefault(False)
        self.connect_button.setFlat(False)
        self.connect_button.setObjectName("connect_button")
        self.gridLayout.addWidget(self.connect_button, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(93, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(94, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 4, 1, 1)
        self.read_file_button = QtGui.QPushButton(DefaultPart)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.read_file_button.sizePolicy().hasHeightForWidth())
        self.read_file_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.read_file_button.setFont(font)
        self.read_file_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.read_file_button.setStyleSheet("QPushButton#read_file_button {\n"
"    font: 20pt \"Arial\";\n"
"    background:qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.05                     #77d42a, stop:1 #5cb811);\n"
"    border-style:outset;\n"
"    border-width:2px;\n"
"    border-radius:12px;\n"
"    border-color:#636363;\n"
"    padding:9px 18px \n"
"}\n"
"\n"
"QPushButton#read_file_button:hover{\n"
"    background:qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.05                     #5cb811, stop:1 #77d42a);\n"
"}\n"
"\n"
"QPushButton#read_file_button:pressed {\n"
"     background: #adff2f;\n"
"     border-style: inset;}")
        self.read_file_button.setIconSize(QtCore.QSize(48, 48))
        self.read_file_button.setAutoRepeat(False)
        self.read_file_button.setDefault(False)
        self.read_file_button.setFlat(False)
        self.read_file_button.setObjectName("read_file_button")
        self.gridLayout.addWidget(self.read_file_button, 0, 3, 1, 1)

        self.retranslateUi(DefaultPart)
        QtCore.QMetaObject.connectSlotsByName(DefaultPart)

    def retranslateUi(self, DefaultPart):
        DefaultPart.setWindowTitle(QtGui.QApplication.translate("DefaultPart", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.connect_button.setText(QtGui.QApplication.translate("DefaultPart", "检测连接", None, QtGui.QApplication.UnicodeUTF8))
        self.connect_button.setShortcut(QtGui.QApplication.translate("DefaultPart", "Ctrl+Alt+L", None, QtGui.QApplication.UnicodeUTF8))
        self.read_file_button.setText(QtGui.QApplication.translate("DefaultPart", "读取文档", None, QtGui.QApplication.UnicodeUTF8))
        self.read_file_button.setShortcut(QtGui.QApplication.translate("DefaultPart", "Ctrl+Alt+R", None, QtGui.QApplication.UnicodeUTF8))

import Icons_rc
