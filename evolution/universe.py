import random
import numpy as np
from evolution.db import CreatureDB
from evolution.creature import Creature
from evolution.environment import Environment

class Universe(object):

    def __init__(self, filename, env, population=500):
        self.db = CreatureDB(filename)
        self.env = env
        self.population = population
        self.alive = set()
        if self.db.count() == 0:
            # start from scratch
            self.make_first_generation()
        else:
            raise NotImplementedError('load from existing DB')

    def make_first_generation(self):
        print 'Creating first generation'
        with self.db.atomic:
            for i in range(self.population):
                c = Creature()
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
        min = np.min(values)
        avg = np.average(values)
        max = np.max(values)
        #
        print 'Generation %3d: min=%9.2f  avg=%9.2f   max=%9.2f' % (self.db.generation, min, avg, max)

    def compute_fitness_one(self, c):
        fitness = self.env.run(c)
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
        N = int(round(self.population * 0.05))
        i10 = int(round(self.population * 0.1))
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

