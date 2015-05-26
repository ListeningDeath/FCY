# -*- coding: utf-8 -*-
from PySide.QtGui import QApplication
from PySide.QtCore import Qt, QTranslator
from ui.MainWindow import MainWindow
import sys
if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator()
    translator.load(":/zh/qt_zh_CN.qm")
    app.installTranslator(translator)
    window = MainWindow()
    #window.setWindowFlags(window.windowFlags() &~ Qt.WindowMinMaxButtonsHint)
    window.setWindowFlags(window.windowFlags() &~ Qt.WindowMaximizeButtonHint)
    #window.setWindowFlags(Qt.FramelessWindowHint)
    window.show()
    sys.exit(app.exec_())

