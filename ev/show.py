import sys
import numpy
import cPickle as pickle
import ev.pypycompat
from ev.environment import Environment

import ev.creature
sys.modules['evolution.creature'] = ev.creature

def main():
    # don't use scientific notation when printing
    numpy.set_printoptions(suppress=True)

    filename = sys.argv[1]
    with open(filename) as f:
        c = pickle.load(f)
    c.reset()

    print 'Matrix'
    print c.matrix
    print
    print 'Constant'
    print c.constant

    #env = Environment(show=True, z1=5, z2=3)
    env = Environment(show=True, z1=5, z2=8)
    fitness = env.run(c)
    print 'fitness:', fitness

if __name__ == '__main__':
    main()
