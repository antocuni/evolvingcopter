import sys
if hasattr(sys, 'pypy_version_info'):
    import evolution.pypycompat
from evolution.environment import Environment


def main():
    import cPickle as pickle
    filename = sys.argv[1]
    with open(filename) as f:
        c = pickle.load(f)
    c.reset()
    env = Environment(show=True, z1=5, z2=3)
    #env = Environment(show=True, z1=5, z2=8)
    print env.run(c)

if __name__ == '__main__':
    main()
