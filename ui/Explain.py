from PySide.QtGui import QWidget
from Ui_Explain import Ui_Explain


class Explain(QWidget, Ui_Explain):
    def __init__(self, parent=None):
        super(Explain, self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    from PySide.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    window = Explain()
    window.show()
    sys.exit(app.exec_())
