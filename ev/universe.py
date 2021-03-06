import random
import numpy as np
from ev.db import CreatureDB
from ev.fakedb import FakeDB
from ev.creature import Creature, SpecializedCreature
from ev.environment import Environment

class Universe(object):

    def __init__(self, filename, envs, population=500, no_specialized=False):
        #self.db = CreatureDB(filename)
        self.db = FakeDB()
        self.envs = envs
        self.population = population
        self.no_specialized = no_specialized
        self.alive = set()
        if self.db.count() == 0:
            # start from scratch
            self.make_first_generation()
        else:
            raise NotImplementedError('load from existing DB')

    def make_first_generation(self):
        print 'Creating first generation'
        if self.no_specialized:
            print 'WARNING: using the slow non-specialized creature'
            make_creature = Creature
        else:
            make_creature = SpecializedCreature
        #
        with self.db.atomic:
            for i in range(self.population):
                c = make_creature()
                self.db.new(c)
                self.alive.add(c)

    def compute_fitness(self):
        """
        Make sure that we computed the fitness of all the alive creatures.
        """
        # we check if the fitness has already been computed. This happens in
        # two cases:
        #
        #   1. at each generation, half of the population survived, and thus
        #      we already know its fitness
        #
        #   2. in case we interrupted the simulation in the middle of
        #      compute_fitness
        values = []
        for c in self.alive:
            fitness = self.db.get_fitness(c)
            if fitness is None:
                fitness = self.compute_fitness_one(c)
            values.append(fitness)
        #
        self.last_min = min(values)
        self.last_avg = sum(values) / len(values)
        self.last_max = max(values)

    def compute_fitness_one(self, c):
        fitness = 0
        for env in self.envs:
            fitness += env.run(c)
        self.db.update_fitness(c, fitness)
        return fitness

    def kill_some(self):
        # first, sort the creatures by fitness (smaller is better)
        creatures = list(self.alive)
        creatures.sort(key=self.db.get_fitness)
        #
        # normally, only the upper half would survive. However, to improve
        # genetic variation, a random 5% surives even if it's in the lower
        # half. We do the following:
        #
        # 1. the best 10% always survives
        # 2. N creatures in the [10%:50%] are killed; the other survive
        # 3. N creatures in the [50%:100%] survives; the other are killed
        #
        N = int(round(self.population * 0.15))   # 15% survives randomly
        i10 = int(round(self.population * 0.01)) # save only the top 1%
        i50 = int(round(self.population * 0.5))
        best = set(creatures[:i10])
        good = set(creatures[i10:i50])
        bad = set(creatures[i50:])
        #
        unlucky = set(random.sample(good, N))
        lucky = set(random.sample(bad, N))
        good.difference_update(unlucky)
        bad.difference_update(lucky)
        survivors = best.union(good).union(lucky)
        killed = bad.union(unlucky)
        #
        assert len(survivors) + len(killed) == self.population
        for c in killed:
            self.db.kill(c)
        self.alive = survivors

    def reproduce(self):
        new_creatures = [c.reproduce() for c in self.alive]
        for c in new_creatures:
            self.db.new(c)
            self.alive.add(c)

    def run_one_generation(self):
        self.compute_fitness()
        self.kill_some()
        self.db.new_generation()
        self.reproduce()

    def save_best(self):
        import cPickle as pickle
        creatures = list(self.alive)
        creatures.sort(key=self.db.get_fitness)
        for c in creatures:
            fitness = self.db.get_fitness(c)
            if fitness is not None:
                best = c
                break
        else:
            print 'something is wrong'
            import pdb;pdb.set_trace()
        #
        filename = 'creature-%.2f-%d.pickle' % (fitness, best.id)
        with open(filename, 'w') as f:
            pickle.dump(best, f)
        print 'best creature saved to', filename

