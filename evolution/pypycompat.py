import sys
import _numpypy
sys.modules['numpy'] = _numpypy.multiarray
np = _numpypy.multiarray

class random(object):

    @staticmethod
    def random(n):
        # XXX implement me
        return np.zeros(n)

    @staticmethod
    def normal(mu, sigma, n):
        return np.zeros(n)

np.random = random
