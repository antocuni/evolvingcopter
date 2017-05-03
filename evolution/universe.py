from evolution.db import CreatureDB
from evolution.creature import Creature
from evolution.environment import Environment

class Universe(object):

    def __init__(self, filename, population=500):
        self.db = CreatureDB(filename)
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

    def run_one_generation(self):
        self.compute_fitness()
        self.kill_some()
        self.db.new_generation()
        self.reproduce()

