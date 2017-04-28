from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys

ARM_LENGTH = 0.086 # meter
HEIGHT = 0.1
L = ARM_LENGTH
H = HEIGHT
BODY_FRAME = np.array([(L, 0, 0, 1),
                       (0, L, 0, 1),
                       (-L, 0, 0, 1),
                       (0, -L, 0, 1),
                       (0, 0, 0, 1),
                       (0, 0, H, 1)])


class QuadPlotter(object):

    def __init__(self):
        self.fig = plt.figure()
        ax = self.fig.add_axes([0, 0, 1, 1], projection='3d')
        ax.plot([], [], [], '-', c='cyan')[0]
        ax.plot([], [], [], '-', c='red')[0]
        ax.plot([], [], [], '-', c='blue', marker='o', markevery=2)[0]
        self.set_limit((-0.5,0.5), (-0.5,0.5), (-0.5,5))

    def set_limit(self, x, y, z):
        ax = plt.gca()
        ax.set_xlim(x)
        ax.set_ylim(y)
        ax.set_zlim(z)

    def plot_animation(self, get_world_frame):
        """
        get_world_frame is a function which return the "next" world frame to be
        drawn
        """
        def anim_callback(i):
            frame = get_world_frame(i)
            self.set_frame(frame)

        an = animation.FuncAnimation(self.fig,
                                     anim_callback,
                                     init_func=None,
                                     frames=400, interval=10, blit=False)
        if len(sys.argv) > 1 and sys.argv[1] == 'save':
            an.save('sim.gif', dpi=80, writer='imagemagick', fps=60)
        else:
            plt.show(block=False)

    def plot_step(self, quad):
        world_frame = self.get_world_frame(quad)
        self.set_frame(world_frame)
        plt.pause(0.00001)

    def set_frame(self, frame):
        # convert 3x6 world_frame matrix into three line_data objects which is 3x2 (row:point index, column:x,y,z)
        lines_data = [frame[:,[0,2]], frame[:,[1,3]], frame[:,[4,5]]]
        ax = plt.gca()
        lines = ax.get_lines()
        for line, line_data in zip(lines, lines_data):
            x, y, z = line_data
            line.set_data(x, y)
            line.set_3d_properties(z)

    def get_world_frame(self, quad):
        x, y, z = quad.position
        origin = x, y, -z
        roll, pitch, yaw = quad.rpy
        rot = RPYToRot(roll, pitch, yaw)
        wHb = np.r_[np.c_[rot,origin], np.array([[0, 0, 0, 1]])]
        quadBodyFrame = BODY_FRAME.T
        quadWorldFrame = wHb.dot(quadBodyFrame)
        world_frame = quadWorldFrame[0:3]
        return world_frame


def RPYToRot(phi, theta, psi):
    """
    phi, theta, psi = roll, pitch , yaw
    """
    from math import sin, cos, asin, atan2, sqrt
    return np.array([[cos(psi)*cos(theta) - sin(phi)*sin(psi)*sin(theta), cos(theta)*sin(psi) + cos(psi)*sin(phi)*sin(theta), -cos(phi)*sin(theta)],
                     [-cos(phi)*sin(psi), cos(phi)*cos(psi), sin(phi)],
                     [cos(psi)*sin(theta) + cos(theta)*sin(phi)*sin(psi), sin(psi)*sin(theta) - cos(psi)*cos(theta)*sin(phi), cos(phi)*cos(theta)]])
