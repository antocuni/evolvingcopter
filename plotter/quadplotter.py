from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np

class QuadPlotter(object):

    def __init__(self, title='Quadcopter', arm_length=2):
        self.arm_length = arm_length
        self.app = QtGui.QApplication([])
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 40
        self.w.setWindowTitle(title)
        self._make_grid()
        self._make_quad()
        self.w.show()
        N = 3
        self.w.resize(640*N, 480*N)
        self.w.move(0, 0)

    def _make_grid(self):
        # make the grid
        gx = gl.GLGridItem()
        gx.rotate(90, 0, 1, 0)
        gx.translate(-10, 0, 0)
        self.w.addItem(gx)
        gy = gl.GLGridItem()
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -10, 0)
        self.w.addItem(gy)
        gz = gl.GLGridItem()
        gz.translate(0, 0, -10)
        self.w.addItem(gz)
        #
        # make the axes
        ax = gl.GLAxisItem()
        ax.setSize(100, 100, 100)
        self.w.addItem(ax)

    def _make_quad(self):
        red = (1, 0, 0)
        cyan = (0, 1, 1)
        yellow = (1, 1, 0)
        green = (0, 1, 0)
        #
        L = self.arm_length
        H = L/8.0
        lines = [
            # from            to             color
            ([  -L,  0,  0], [-L+H,  0,  0], red),    # indicate the norh
            ([-L+H,  0,  0], [   L,  0,  0], cyan),   # north-south arm
            ([   0, -L,  0], [   0,  L,  0], yellow), # west-east arm
            ([   0,  0,  0], [   0,  0,  H], green),
        ]
        points = []
        colors = []
        for a, b, color in lines:
            points.append(a)
            points.append(b)
            colors.append(color)
            colors.append(color)
        #
        self.quad = gl.GLLinePlotItem(pos=np.array(points),
                                      color=np.array(colors),
                                      mode='lines',
                                      width=3)
        self.w.addItem(self.quad)

    def update(self, pos, rpy):
        """
        Set the new position and rotation of the quadcopter: ``pos`` is a tuple
        (x, y, z), and rpy is a tuple (roll, pitch, yaw) expressed in
        *radians*
        """
        self.quad.resetTransform()
        x, y, z = pos
        self.quad.translate(x, y, -z) # invert the z axis
        roll, pitch, yaw = np.rad2deg(rpy)
        self.quad.rotate(roll, 1, 0, 0, local=True)
        self.quad.rotate(pitch, 0, 1, 0, local=True)
        self.quad.rotate(yaw, 0, 0, 1, local=True)

    def show_step(self, dt=0.01):
        if not self.w.isVisible():
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
