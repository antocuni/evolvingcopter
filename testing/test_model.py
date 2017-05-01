from pytest import approx
from model import _qrmod
from model.quadcopter import Quadcopter

def test_qrmod():
    st = _qrmod.ffi.new('qrstate_t*')
    _qrmod.lib.qr_init(st, 0, 1, 1)
    assert st.t == 0
    _qrmod.lib.qr_nextstate(st, 0.5)
    assert st.t == 0.5

class TestQuadcopter(object):

    def test_run_reset(self):
        quad = Quadcopter()
        assert quad.t == 0
        quad.run(t=1)
        assert quad.t == approx(1)
        quad.reset()
        assert quad.t == 0

    def test_lift(self):
        quad = Quadcopter(mass=0.5, motor_thrust=0.5)
        assert quad.position == (0, 0, 0)
        assert quad.rpy == (0, 0, 0)
        #
        # power all the motors, to lift the quad vertically. The motors give a
        # total acceleration of 4g. Considering the gravity, we have a total
        # net acceleration of 3g.
        t = 1 # second
        g = 9.81 # m/s**2
        z = 0.5 * (3*g) * t**2  # d = 1/2 * a * t**2
        #
        quad.set_thrust(1, 1, 1, 1)
        quad.run(t=1, dt=0.0001)
        pos = quad.position
        assert pos.x == 0
        assert pos.y == 0
        assert pos.z == approx(z, rel=1e-3) # the simulated z is a bit
                                            # different than the computed one
        assert quad.rpy == (0, 0, 0)

    def test_Quadcopter_yaw(self):
        quad = Quadcopter()
        # only two motors on, to produce a yaw
        quad.set_thrust(0, 10, 0, 10)
        quad.run(t=1)
        assert quad.rpy.yaw > 0
        assert quad.rpy.pitch == 0
        assert quad.rpy.roll == 0
        #
        # now try to yaw in the opposite direction
        quad.reset()
        quad.set_thrust(10, 0, 10, 0)
        quad.run(t=1)
        assert quad.rpy.yaw < 0
        assert quad.rpy.pitch == 0
        assert quad.rpy.roll == 0
