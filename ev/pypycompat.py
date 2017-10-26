import sys
IS_PYPY = hasattr(sys, 'pypy_version_info')
if IS_PYPY:
    if '--no-numpypy' in sys.argv:
        print 'numpypy switched off by command line option'
        USE_NUMPYPY = False
    else:
        USE_NUMPYPY = True
else:
    # CPython
    USE_NUMPYPY = False

if USE_NUMPYPY:
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
        def _reconstruct(t, shape, dtype):
            return numpy.empty(shape, dtype=dtype)

        @staticmethod
        def scalar(dtype, buf):
            arr = numpy.frombuffer(buf, dtype=dtype)
            return arr[0]

    sys.modules['_numpypy.multiarray'] = fake_numpypy
