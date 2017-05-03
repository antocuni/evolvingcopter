import time
from evolution.creature import Creature
from evolution.environment import Environment
from evolution.universe import Universe

DB = 'creatures.db'

def main():
    env = Environment(show=False)
    uni = Universe(DB, env, population=10)
    try:
        while True:
            uni.run_one_generation()
    except KeyboardInterrupt:
        import pdb;pdb.set_trace()


def main2():
    #
    # create many creatures
    env = Environment(show=False)
    creatures = []
    print 'running simulation...'
    for i in range(50):
        c = Creature(i)
        fitness = env.run(c)
        creatures.append((fitness, c))

    creatures.sort()
    for fitness, c in creatures:
        print fitness, c.id

    # show the best
    show_env = Environment(show=True)
    fitness, c = creatures[0]
    show_env.run(c)

if __name__ == '__main__':
    main()
