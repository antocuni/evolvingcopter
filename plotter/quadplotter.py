from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np

RED = (1, 0, 0)
CYAN = (0, 1, 1)
YELLOW = (1, 1, 0)
GREEN = (0, 1, 0)


class QuadPlotter(object):

    def __init__(self, title='Quadcopter', arm_length=2):
        self.arm_length = arm_length
        self.app = QtGui.QApplication([])
        self._make_glview()
        self._make_layout()
        self.win.setWindowTitle(title)
        self.win.show()
        N = 3
        self.win.resize(640*N, 480*N)
        self.win.move(0, 0)

    def _make_layout(self):
        self.win = QtGui.QWidget()
        layout = QtGui.QGridLayout()
        self.win.setLayout(layout)
        #
        self.label_t = QtGui.QLabel()
        self.label_t.setAlignment(QtCore.Qt.AlignRight)
        self.glview.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                  QtGui.QSizePolicy.Expanding)
        #
        layout.addWidget(self.glview, 0, 0)
        layout.addWidget(self.label_t, 1, 0)

    def _make_glview(self):
        self.glview = gl.GLViewWidget()
        self.glview.opts['distance'] = 40
        #self.glview.pan(dx=0, dy=0, dz=100)
        self._make_grid()
        self._make_quad()

    def _make_grid(self):
        # make the grid
        gx = gl.GLGridItem()
        gx.rotate(90, 0, 1, 0)
        gx.translate(-10, 0, 0)
        self.glview.addItem(gx)
        gy = gl.GLGridItem()
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -10, 0)
        self.glview.addItem(gy)
        gz = gl.GLGridItem()
        gz.translate(0, 0, -10)
        self.glview.addItem(gz)
        #
        # make the axes
        ax = gl.GLAxisItem()
        ax.setSize(100, 100, 100)
        self.glview.addItem(ax)

    def _make_quad(self):
        L = self.arm_length
        H = L/8.0
        lines = [
            # from            to             color
            ([  -L,  0,  0], [-L+H,  0,  0], RED),    # indicate the norh
            ([-L+H,  0,  0], [   L,  0,  0], CYAN),   # north-south arm
            ([   0, -L,  0], [   0,  L,  0], YELLOW), # west-east arm
            ([   0,  0,  0], [   0,  0,  H], GREEN),
        ]
        points = []
        colors = []
        for a, b, color in lines:
            points.append(a)
            points.append(b)
            colors.append(color)
            colors.append(color)
        #
        self.quadplot = gl.GLLinePlotItem(pos=np.array(points),
                                          color=np.array(colors),
                                          mode='lines',
                                          width=3)
        self.glview.addItem(self.quadplot)

    def add_marker(self, pos, color, size=0.1):
        points = np.array([pos])
        p = gl.GLScatterPlotItem(pos=points,
                                 color=np.array(color),
                                 size=size,
                                 pxMode=False)
        self.glview.addItem(p)

    def update(self, quad):
        """
        Set the new position and rotation of the quadcopter: ``pos`` is a tuple
        (x, y, z), and rpy is a tuple (roll, pitch, yaw) expressed in
        *radians*
        """
        x, y, z = quad.position
        roll, pitch, yaw = np.rad2deg(quad.rpy)
        self.quadplot.resetTransform()
        self.quadplot.translate(x, y, z)
        self.quadplot.rotate(roll, 1, 0, 0, local=True)
        self.quadplot.rotate(pitch, 0, 1, 0, local=True)
        self.quadplot.rotate(yaw, 0, 0, 1, local=True)
        #
        self.label_t.setText('t = %5.2f' % quad.t)

    def show_step(self, dt=0.01):
        if not self.win.isVisible():
            return False
        self.app.processEvents(QtCore.QEventLoop.AllEvents, 0.01)
        return True

    def show(self):
        self.app.exec_()

if __name__ == '__main__':
    import math
    x, y, z = 0, 0, 0
    roll, pitch, yaw = 0, 0, 0
    plot = QuadPlotter()
    while plot.show_step():
        x += 0.01
        yaw = math.sin(x)
        plot.update(pos=(x, y, z), rpy=(roll, pitch, yaw))
