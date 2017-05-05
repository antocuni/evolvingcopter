import sys
import random
import _numpypy
sys.modules['numpy'] = _numpypy.multiarray
np = _numpypy.multiarray

class np_random(object):

    @staticmethod
    def random(n):
        result = np.empty(n)
        values = result.ravel()
        for i in range(len(values)):
            values[i] = random.random()
        return result

    @staticmethod
    def normal(mu, sigma, n):
        result = np.empty(n)
        values = result.ravel()
        for i in range(len(values)):
            values[i] = random.gauss(mu, sigma)
        return result

np.random = np_random
