from collections import namedtuple
from model import _qrmod

Point = namedtuple('Point', ['x', 'y', 'z'])
RPY = namedtuple('RPY', ['roll', 'pitch', 'yaw'])

class Quadcopter(object):

    def __init__(self, mass=1.0, motor_thrust=1.0):
        self.mass = mass
        self.motor_thrust = motor_thrust
        self.reset()

    def reset(self):
        self.qr = _qrmod.ffi.new('qrstate_t*')
        _qrmod.lib.qr_init(self.qr, 0, self.mass, self.motor_thrust)

    def run(self, t, dt=0.001):
        elapsed = 0
        while elapsed < t:
            self.step(dt)
            elapsed += dt

    def step(self, dt):
        _qrmod.lib.qr_nextstate(self.qr, dt)

    @property
    def t(self):
        return self.qr.t

    @property
    def position(self):
        # qrmod has a Z axis which goes "down". Invert it so that it goes "up"
        return Point(self.qr.x, self.qr.y, -self.qr.z)

    @position.setter
    def position(self, pos):
        x, y, z = pos
        self.qr.x = x
        self.qr.y = y
        self.qr.z = -z # invert the z

    @property
    def rpy(self):
        return RPY(self.qr.phi, self.qr.theta, self.qr.psi)

    def set_thrust(self, a1, a2, a3, a4):
        self.qr.a1 = max(0, a1)
        self.qr.a2 = max(0, a2)
        self.qr.a3 = max(0, a3)
        self.qr.a4 = max(0, a4)
