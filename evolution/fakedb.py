class FakeTransaction(object):
    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass

class FakeDB(object):

    def __init__(self):
        self.lastid = 0
        self.generation = 0

    def count(self):
        return 0

    atomic = FakeTransaction()

    def new_generation(self):
        self.generation += 1

    def new(self, c):
        self.lastid += 1
        c.id = self.lastid
        c.born_at = self.generation
        return c

    def get_fitness(self, c):
        return getattr(c, 'fitness', None)

    def update_fitness(self, c, fitness):
        c.fitness = fitness

    def kill(self, c):
        pass
