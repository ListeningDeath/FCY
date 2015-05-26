# -*- coding: utf-8 -*-
from PySide.QtGui import QWidget
from Ui_DefaultPart import Ui_DefaultPart


class DefaultPart(QWidget, Ui_DefaultPart):
    def __init__(self, parent=None):
        super(DefaultPart, self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    from PySide.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    window = DefaultPart()
    window.show()
    sys.exit(app.exec_())
