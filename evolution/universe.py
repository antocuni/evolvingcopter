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
        for c in self.alive:
            fitness = self.db.get_fitness(c)
            if fitness is None:
                self.compute_fitness_one(c)

    def compute_fitness_one(self, c):
        fitness = self.env.run(c)
        self.db.update_fitness(c, fitness)

    def run_one_generation(self):
        self.compute_fitness()
        self.kill_some()
        self.db.new_generation()
        self.reproduce()

