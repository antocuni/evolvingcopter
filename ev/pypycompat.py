import sys
IS_PYPY = hasattr(sys, 'pypy_version_info')
if IS_PYPY:
    # make sure that 'import numpy' imports _numpypy.multiarray
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

else:
    # make it possible to unpickle numpypy arrays in CPython
    import numpy
    class fake_numpypy(object):

        @staticmethod
        def _reconstruct(self, shape, dtype):
            return numpy.empty(shape, dtype=dtype)

    sys.modules['_numpypy.multiarray'] = fake_numpypy
