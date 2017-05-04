import time
import sys
if hasattr(sys, 'pypy_version_info'):
    import evolution.pypycompat
from evolution.creature import Creature
from evolution.environment import Environment
from evolution.universe import Universe


DB = 'creatures.db'

def main():
    env = Environment(show=False)
    uni = Universe(DB, env, population=500)
    while True:
        a = time.time()
        uni.run_one_generation()
        b = time.time()
        print '   %.2f secs' % (b-a)
        print


def show_best():
    from evolution.db import CreatureDB
    db = CreatureDB('creatures.db.200')
    c = db.load_best()
    c.reset()
    show_env = Environment(show=True) #, z1=2, z2=4)
    print show_env.run(c)


if __name__ == '__main__':
    main()
    #show_best()
