import time
import sys
import ev.pypycompat
from ev.creature import Creature
from ev.environment import Environment
from ev.universe import Universe

DB = 'creatures.db'

def main():
    envs = [Environment(z1=5, z2=3),
            Environment(z1=5, z2=8),
            Environment(z1=10, z2=10)]
    uni = Universe(DB, envs, population=500)
    while True:
        try:
            a = time.time()
            uni.run_one_generation()
            b = time.time()
            print '   %.2f secs' % (b-a)
            print
        except KeyboardInterrupt:
            print 'Saving the best so far...'
            uni.save_best()
            print 'Press CTRL-C in the next 2 seconds to exit'
            try:
                time.sleep(2)
            except KeyboardInterrupt:
                break

if __name__ == '__main__':
    main()
