import time
import sys
if hasattr(sys, 'pypy_version_info'):
    import ev.pypycompat
from ev.creature import Creature
from ev.environment import Environment
from ev.universe import Universe

DB = 'creatures.db'

def main():
    envs = [Environment(z1=5, z2=3),
            Environment(z1=5, z2=8)]
    uni = Universe(DB, envs, population=500)
    try:
        while True:
            a = time.time()
            uni.run_one_generation()
            b = time.time()
            print '   %.2f secs' % (b-a)
            print
    finally:
        uni.save_best()

if __name__ == '__main__':
    main()
