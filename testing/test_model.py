from pytest import approx
from model import _qrmod
from model.quadcopter import Quadcopter

def test_qrmod():
    st = _qrmod.ffi.new('qrstate_t*')
    _qrmod.lib.qr_init(st, 0)
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
        quad = Quadcopter()
        assert quad.position == (0, 0, 0)
        assert quad.rpy == (0, 0, 0)
        #
        # power all the motors, to lift the quad vertically
        quad.set_thrust(10, 10, 10, 10)
        quad.run(t=1)
        #
        pos = quad.position
        assert pos.x == 0
        assert pos.y == 0
        assert pos.z < 0 # check that the quad lifted a bit
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
