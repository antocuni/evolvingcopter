import pytest
import itertools
from evolution.universe import Universe

@pytest.fixture
def filename(tmpdir):
    return str(tmpdir.join('creatures.db'))

class FakeEnv(object):

    def __init__(self):
        self._fitness = itertools.count(0)

    def run(self, c):
        return next(self._fitness)

def test_first_generation(filename):
    uni = Universe(filename, env=None, population=10)
    assert len(uni.alive) == 10
    ids = [c.id for c in uni.alive]
    assert sorted(ids) == range(1, 11)
    for c in uni.alive:
        assert uni.db.get_fitness(c) is None


def test_compute_fitness(filename):
    uni = Universe(filename, env=FakeEnv(), population=5)
    uni.compute_fitness()
    #
    for i, c in enumerate(uni.alive):
        fitness = uni.db.get_fitness(c)
        assert fitness == i

def test_compute_fitness_partial(filename):
    uni = Universe(filename, env=FakeEnv(), population=5)
    creatures = list(uni.alive)
    creatures.sort(key=lambda c: c.id)
    c1, c2, c3, c4, c5 = creatures
    #
    # manually compute the fitness for c1 and c2
    uni.db.update_fitness(c1, 10)
    uni.db.update_fitness(c2, 20)
    #
    computed = set()
    uni.compute_fitness_one = computed.add
    uni.compute_fitness()
    assert computed == set([c3, c4, c5])


