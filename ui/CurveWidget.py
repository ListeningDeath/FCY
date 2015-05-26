# -*- coding:utf8
from curve.MplCanvas import MplCanvas
from matplotlib.widgets import Cursor, MultiCursor
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from PySide.QtCore import Qt, Signal


class CurveWidget(MplCanvas):
    lcd_signal = Signal(tuple)

    def __init__(self, parent=None):
        super(CurveWidget, self).__init__(parent)
        self.clearAxisGroup()
        self.setupValue()
        #self.produceAxis((0, 1, 2, 10, 11))
        self.setupConnect()

    def setupValue(self):
        self.color_sheet = ['#0000ff', '#ff0000', '#ffff00', '#00ff40', '#00ffff', '#0080c0', '#8080c0',
                          '#ff00ff', '#800000', '#ff8000', '#008040', '#800080', 'black']
        self.text_sheet = ['P1(MPa)', 'P2(MPa)', 'P3(MPa)', 'P4(MPa)', 'P5(MPa)', 'P6(MPa)', 'D1', 'D2',
                           'D3', 'D4', 'v(m/s)', 'a(g)', 's(m)']
        self.setCursor(Qt.CrossCursor)
        #用于计算放大和缩小
        self.count = 0

    def setupConnect(self):
        """
        建立鼠标的监听事件
        """
        self.move_event = self.canvas.mpl_connect('motion_notify_event', self.onMplMove)
        self.press_event = self.canvas.mpl_connect('button_press_event', self.onMplClickPress)
        self.scroll_event = self.canvas.mpl_connect('scroll_event', self.onMplScroll)
        self.release_event = self.canvas.mpl_connect('button_release_event', self.onMplClickRelease)

    def cancelConnect(self):
        """
        建立鼠标的监听事件
        """
        self.canvas.mpl_disconnect(self.move_event)
        self.canvas.mpl_disconnect(self.press_event)
        self.canvas.mpl_disconnect(self.scroll_event)
        self.canvas.mpl_disconnect(self.release_event)

    def clearAxisGroup(self):
        self.axis_group = []
        self.axis_lines = []
        self.text_group = []

    def clear(self):
        self.clearAxisGroup()
        #self.cur_axes.cla()
        self.fig.clf()
        self._init_Axes()

    def drawLine2D(self, index, x_data, y_data, color):
        """曲线集合"""
        line2D, = self.axis_group[index].plot(x_data, y_data, color=color)
        self.axis_lines.append(line2D)
        #print 'index', index

    def setXFull(self, left, right):
        self.axes.set_xlim(left, right)

    def updateDraw(self):
        self.canvas.draw()
        self.canvas.draw_idle()

    def produceAxis(self, exist_axis):
        """根据args确定绘制那些图像"""
        self.clearAxisGroup()
        self.exist_axis = exist_axis
        #print exist_axis
        number = len(self.exist_axis)
        if number > 1:
            space = 1.0 / (number - 1)
        else:
            space = 1
        majorFormatter = FormatStrFormatter('%0.1f')
        for i in range(number):
            if i == 0:
                ax = self.axes.twinx()
                self.axis_group.append(ax)
            else:
                ax = self.axis_group[i - 1].twinx()
                self.axis_group.append(ax)
        #同时创建最上层界面
        if self.axis_group:
            self.cur_axes = self.axis_group[-1].twinx()
        else:
            self.cur_axes = self.axes.twinx()
        self.cur_axes.yaxis.set_visible(False)
        self.cur_axes.tick_params(axis='y', left='off', labelleft='off', width=0)
        self.cursor = Cursor(self.cur_axes, useblit=True, color='gray', linewidth=0.5, linestyle='--')
        self.crossingLine(self.cur_axes)

        for i, j in enumerate(self.exist_axis):
            text = self.axes.text(i * space, 1.02, self.text_sheet[j], transform=self.axes.transAxes,
                                  color=self.color_sheet[j], fontsize='medium')
            self.text_group.append(text)
            ax = self.axis_group[i]
            ax.spines["left"].set_color(self.color_sheet[j])
            ax.spines["left"].set_position(('axes', space * i))
            self.make_patch_spines_invisible(ax)
            ax.spines["left"].set_visible(True)
            ax.spines['left'].set_lw(0.5)
            #解决
            ax.tick_params(axis='y', colors=self.color_sheet[j], direction='in', pad=-20, labelsize=8)
            ax.tick_params(axis='y', colors=self.color_sheet[j], which='minor', direction='in')
            ax.yaxis.set_major_formatter(majorFormatter)
            if j < 6:
                continue
            elif j < 10:
                majorLocator = MultipleLocator(1.0)
                ax.yaxis.set_major_locator(majorLocator)
                minorLocator = MultipleLocator(0.1)
                ax.yaxis.set_minor_locator(minorLocator)
                ax.set_ylim(-0.5, 5)
                ax.yaxis.set_ticklabels([])
            elif j == 10:
                majorLocator = MultipleLocator(7.0)
                ax.yaxis.set_major_locator(majorLocator)
                minorLocator = MultipleLocator(0.7)
                ax.yaxis.set_minor_locator(minorLocator)
                ax.set_ylim(-3.5, 35)
            elif j == 11:
                majorLocator = MultipleLocator(5.0)
                ax.yaxis.set_major_locator(majorLocator)
                minorLocator = MultipleLocator(0.5)
                ax.yaxis.set_minor_locator(minorLocator)
                ax.set_ylim(-7.5, 20)
            self.axis_group.append(ax)

    def make_patch_spines_invisible(self, ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.itervalues():
            sp.set_visible(False)

    def crossingLine(self, cur_ax):
        """十字线"""
        self.lx = cur_ax.axhline(y=None, color='g', ls='--', lw=0.4)
        self.ly = cur_ax.axvline(x=None, color='g', ls='--', lw=0.4)

    def setTicker(self, axis_num, interval):
        """设置刻度属性0-5, 12"""
        #_sheet = [[0, 1], [0, 5], [0, 10]] #区间表
        if axis_num not in [0, 1, 2, 3, 4, 5, 12]:
            return
        index = self.exist_axis.index(axis_num)
        if interval == 0:
            majorLocator = MultipleLocator(8)
            self.axis_group[index].yaxis.set_major_locator(majorLocator)
            minorLocator = MultipleLocator(0.8)
            self.axis_group[index].yaxis.set_minor_locator(minorLocator)
            self.axis_group[index].set_ylim(-4, 40)
        elif interval == 1:
            majorLocator = MultipleLocator(2)
            self.axis_group[index].yaxis.set_major_locator(majorLocator)
            minorLocator = MultipleLocator(0.2)
            self.axis_group[index].yaxis.set_minor_locator(minorLocator)
            self.axis_group[index].set_ylim(-1, 10)
        elif interval == 2:
            majorLocator = MultipleLocator(1)
            self.axis_group[index].yaxis.set_major_locator(majorLocator)
            minorLocator = MultipleLocator(0.1)
            self.axis_group[index].yaxis.set_minor_locator(minorLocator)
            self.axis_group[index].set_ylim(-0.5, 5)
        elif interval == 3:
            majorLocator = MultipleLocator(0.4)
            self.axis_group[index].yaxis.set_major_locator(majorLocator)
            minorLocator = MultipleLocator(0.04)
            self.axis_group[index].yaxis.set_minor_locator(minorLocator)
            self.axis_group[index].set_ylim(-0.2, 2)
        elif interval == 4:
            majorLocator = MultipleLocator(0.2)
            self.axis_group[index].yaxis.set_major_locator(majorLocator)
            minorLocator = MultipleLocator(0.02)
            self.axis_group[index].yaxis.set_minor_locator(minorLocator)
            self.axis_group[index].set_ylim(-0.1, 1)

    def setLinesDisplay(self, num, chk_state):
        """
        根据需要调整哪条曲线需要显示
        """
        if not self.axis_lines:
            return
        index = self.exist_axis.index(num)
        self.axis_lines[index].set_visible(chk_state)
        #self.axis_group[index].spines["right"].set_visible(chk_state)
        self.axis_group[index].yaxis.set_visible(chk_state)
        self.text_group[index].set_visible(chk_state)
        self.axis_group[index].set_visible(chk_state)
        self.canvas.draw()

    def setupKey(self, flag):
        """
        监听键盘和鼠标事件
        """
        self.key_flag = flag

    def setShiftTimeChange(self, S_TFlag):
        """
        S-T的转换
        """
        if S_TFlag:
            shift_xdata, shift_ydata = self.axis_lines[-1].get_data()
            self.shift_yaxis = self.axis_group[-1].get_ylim()
            left = float(shift_ydata[0])
            right = float(shift_ydata[-1])
            if left == right:
                return  False
            self.axes.set_xlabel(u'位移(m)')
            self.text_group[-1].set_text("t(s)")
            self.axis_lines[-1].set_data(shift_ydata, shift_xdata)
            for i, j in enumerate(self.axis_lines[:-1]):
                xdata, ydata = j.get_data()
                self.axis_lines[i].set_data(shift_ydata, ydata)
            #yaxis limit
            top = int(float(shift_xdata[-1])) + 1
            bottom = 0
            tb_major = (top - bottom) / 5.0
            majorLocator = MultipleLocator(tb_major)
            self.axis_group[-1].yaxis.set_major_locator(majorLocator)
            tb_minor = tb_major / 10.0
            minorLocator = MultipleLocator(tb_minor)
            self.axis_group[-1].yaxis.set_minor_locator(minorLocator)
            self.axis_group[-1].set_ylim(bottom - 5 * tb_minor, top)
            #xaxis limit
            self.cur_axes.set_xlim(left, right)
            #self.cancelConnect()
        else:
            self.axes.set_xlabel(u'时间(s)')
            self.text_group[-1].set_text("s(m)")
            shift_xdata, shift_ydata = self.axis_lines[-1].get_data()
            left = float(shift_ydata[0])
            right = float(shift_ydata[-1])
            self.axis_lines[-1].set_data(shift_ydata, shift_xdata)
            for i, j in enumerate(self.axis_lines[:-1]):
                xdata, ydata = j.get_data()
                self.axis_lines[i].set_data(shift_ydata, ydata)
            #yaxis limit
            if self.shift_yaxis[1] - self.shift_yaxis[0] > 1:
                self.setTicker(12, 1)
            else:
                self.setTicker(12, 4)
            #xaxis limit
            self.cur_axes.set_xlim(left, right)
            #self.setupConnect()
        self._init_View()
        self.updateDraw()
        return True

    def home(self):
        self.count = 0
        self.mpl_toolbar.home()

    def onMplMove(self, event):
        """
       lcd number is changing with mouse moving
       """
        if not event.inaxes:
            return
        if not self.axis_lines:
            return
        x, y = event.xdata, event.ydata
        #寻找所有的曲线对象，一次发射信号
        x_data, y_data = self.axis_lines[0].get_data()
        for index, j in enumerate(x_data):
            if float(j) > x:
                break
        for i, j in enumerate(self.exist_axis):
            _x, _y = self.axis_lines[i].get_data()
            self.lcd_signal.emit((j, '%5.2f' % float(_y[index])))

        #for i, j in enumerate(self.exist_axis):
            #xy = self.cur_axes.transData.transform((x, y))
            #inv = self.axis_group[i].transData.inverted()
            #_x, _y = inv.transform(xy)
            #self.lcd_signal.emit((j, _y))

    def onMplClickPress(self, event):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        if event.button == 3:
            #if self.mpl_toolbar.isVisible():
                #self.mpl_toolbar.hide()
            #else:
                #self.mpl_toolbar.show()
            self.home()
        elif event.button == 1:
            _x_left, _x_right = self.cur_axes.get_xlim()
            _y_bottom, _y_top = self.cur_axes.get_ylim()
            if self.count <= 0 or _x_left <= self.x_left or _x_right >= self.x_right or _y_bottom <= self.y_bottom or _y_top >= self.y_top:
                return
            self.setCursor(Qt.ClosedHandCursor)
            self.mpl_toolbar.press_pan(event)
            #self.ly.set_xdata(x)
            #self.lx.set_ydata(y)
        self.canvas.draw()

    def onMplClickRelease(self, event):
        if not event.inaxes:
            return
        if event.button == 1:
            self.setCursor(Qt.CrossCursor)
            self.mpl_toolbar.release_pan(event)
            #print self.cur_axes.get_xlim()
            #self.ly.set_xdata(None)
            #self.lx.set_ydata(None)
        self.canvas.draw()

    def onMplScroll(self, event):
        if not event.inaxes:
            return
        #print self.count
        x, y = event.xdata, event.ydata
        #缩小
        if event.button == 'up':
            if self.count >= 20:
                return
            for i, ax in enumerate(self.fig.get_axes()):
                x_min, x_max = ax.get_xlim()
                ax.set_xlim(x_min + (x - x_min) * 0.1, x_max - (x_max - x) * 0.1)
                y_min, y_max = ax.get_ylim()
                ax.set_ylim(y_min + (y - y_min) * 0.1, y_max - (y_max - y) * 0.1)
            self.count += 1
        #放大
        elif event.button == 'down':

            if self.count <= 0:
                return
            for i, ax in enumerate(self.fig.get_axes()):
                x_min, x_max = ax.get_xlim()
                ax.set_xlim(x_min - (x - x_min) * 0.1, x_max + (x_max - x) * 0.1)
                y_min, y_max = ax.get_ylim()
                ax.set_ylim(y_min - (y - y_min) * 0.1, y_max + (y_max - y) * 0.1)
            self.count -= 1
        self.canvas.draw()


if __name__ == "__main__":
    from PySide.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    window = CurveWidget()
    window.show()
    sys.exit(app.exec_())
