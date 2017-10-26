"""
Usage: main [options]

Build a population of creatures and evolve them to adapt to the given
environment.

Options:
  -n N              Initial population count [Default: 500]
  --no-numpypy      Force using the standard numpy even on PyPy
  --no-specialized  Don't use the faster SpecializedCreature
"""

import time
import sys
import docopt
import ev.pypycompat
from ev.creature import Creature
from ev.environment import Environment
from ev.universe import Universe

DB = 'creatures.db'

def main():
    args = docopt.docopt(__doc__)
    population = int(args['-n'])
    no_specialized = args['--no-specialized']
    #
    # use envs in which z1-z0 is similar, but their absolute value is very
    # different, to avoid too much hard-coding in the matrices
    envs = [Environment(z0=3, z1=5),
            Environment(z0=5, z1=3),
            Environment(z0=100, z1=102),
            Environment(z0=302, z1=300),
            Environment(z0=50, z1=60, total_t=4)]
    uni = Universe(DB, envs, population=population,
                   no_specialized=no_specialized)
    while True:
        try:
            a = time.time()
            uni.run_one_generation()
            b = time.time()
            elapsed = b-a
            print ('Generation %3d: min =%9.2f avg =%9.2f '
                   'max =%9.2f  [population = %d]  [%.2f secs]' % (
                       uni.db.generation,
                       uni.last_min,
                       uni.last_avg,
                       uni.last_max,
                       len(uni.alive),
                       elapsed))
        except KeyboardInterrupt:
            print
            print 'Saving the best so far...'
            uni.save_best()
            print 'Press CTRL-C in the next 2 seconds to exit'
            try:
                time.sleep(2)
            except KeyboardInterrupt:
                print
                break

if __name__ == '__main__':
    main()
