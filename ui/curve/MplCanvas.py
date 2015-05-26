# -*- coding:utf8
from PySide.QtGui import QWidget, QVBoxLayout, QSizePolicy
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = 'PySide'
matplotlib.rcParams['font.size'] = 9
matplotlib.rcParams['font.serif'] = ['SimHei']
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['axes.unicode_minus'] = False
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import os
import sys


class MplCanvas(QWidget):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None):
        super(MplCanvas, self).__init__(parent)
        #屏幕图片分辨率
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)
        self.canvas.setParent(parent)
        #调整画布区
        self.fig.subplots_adjust(left=0.02, bottom=0.08, top=0.95, right=0.95)
        self.fig.clear()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.canvas)
        self.mpl_toolbar = NavigationToolbar(self.canvas, parent, coordinates=False)
        #self._init_MplToolBar()
        self.mpl_toolbar.hide()
        #self.layout.addWidget(self.mpl_toolbar)
        self.setLayout(self.layout)
        self._init_Axes()

    def _init_MplToolBar(self):
        """设置toolbar上的功能键"""
        a = self.mpl_toolbar.actions()
        for i in a:
            if i.iconText() == 'Home':
                i.setToolTip(u'初始视图')
            elif i.iconText() == 'Back':
                i.setToolTip(u'后退')
            elif i.iconText() == 'Forward':
                i.setToolTip(u'前进')
            elif i.iconText() == 'Pan':
                i.setToolTip(u'鼠标左键平移，右键横竖缩放')
            elif i.iconText() == 'Zoom':
                i.setToolTip(u'局部缩放')
            elif i.iconText() == 'Subplots':
                self.mpl_toolbar.removeAction(i)
            elif i.iconText() == 'Customize':
                self.mpl_toolbar.removeAction(i)
            elif i.iconText() == 'Save':
                i.setToolTip(u'保存图片')

    def _init_Axes(self):
        self.axes = self.fig.add_subplot(111)
        self.axes.yaxis.set_visible(False)
        #self.axes.tick_params(axis='y', left='off', labelleft='off', width=0)
        self.axes.tick_params(axis='x', top='off')
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['left'].set_visible(False)
        self.axes.spines['bottom'].set_visible(True)
        self.axes.set_xlabel(u'时间(s)')
        self.cur_axes = self.axes
        self.x_left, self.x_right = self.cur_axes.get_xlim()
        self.y_bottom, self.y_top = self.cur_axes.get_ylim()

    def _init_View(self):
        """
        记录当前canvas
        """
        self.mpl_toolbar.update()
        self.mpl_toolbar.push_current()
        self.x_left, self.x_right = self.cur_axes.get_xlim()
        self.y_bottom, self.y_top = self.cur_axes.get_ylim()






if __name__ == "__main__":
    from PySide.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    window = MplCanvas()
    window.resize(800, 600)
    window.show()
    print window.getContentsMargins()
    print window.size()
    print window.canvas.size()
    sys.exit(app.exec_())

