import time
from evolution.creature import Creature
from evolution.environment import Environment

def main():
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
