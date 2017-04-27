from model import _qrmod

def test_qrmod():
    st = _qrmod.ffi.new('qrstate_t*')
    _qrmod.lib.qr_init(st, 0)
    assert st.t == 0
    _qrmod.lib.qr_nextstate(st, 0.5)
    assert st.t == 0.5
