# -*- coding:utf8
import os
import matplotlib
matplotlib.rcParams['backend.qt4'] = 'PySide'
from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.backends.qt4_compat import QtCore, QtGui, _getSaveFileName
from PySide.QtGui import QDockWidget, QVBoxLayout, QToolButton


class ToolBar(NavigationToolbar2, QDockWidget):

    def __init__(self, canvas, parent, coordinates=True):
        """ coordinates: should we show the coordinates on the right? """
        self.canvas = canvas
        self.coordinates = coordinates
        QDockWidget.__init__(self, parent)
        self.setFloating(True)
        NavigationToolbar2.__init__(self, canvas)

    def _icon(self, name):
        return QtGui.QIcon(os.path.join(self.basedir, name))

    def _init_toolbar(self):
        self.basedir = os.path.join(matplotlib.rcParams['datapath'], 'images')

        layout = QVBoxLayout(self)
        #a = QToolButton(self._icon('home.png'), u'原状', self.home)
        a = QToolButton(self)
        layout.addWidget(a)
        a.setToolTip(u'恢复初始状态')
        #a = QToolButton(self._icon('back.png'), u'后退', self.back)
        a = QToolButton(self)
        layout.addWidget(a)
        a.setToolTip(u'前一个视图')
        #a = QToolButton(self._icon('forward.png'), u'前进', self.forward)
        a = QToolButton(self)
        layout.addWidget(a)
        a.setToolTip(u'下一个视图')
        #a = QToolButton(self._icon('move.png'), u'平移', self.pan)
        a = QToolButton(self)
        layout.addWidget(a)
        a.setToolTip('Pan axes with left mouse, zoom with right')
        #a = QToolButton(self._icon('zoom_to_rect.png'), 'Zoom', self.zoom)
        a = QToolButton(self)
        layout.addWidget(a)
        a.setToolTip('Zoom to rectangle')

if __name__ == "__main__":
    from PySide.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    window = ToolBar()
    window.show()
    sys.exit(app.exec_())
