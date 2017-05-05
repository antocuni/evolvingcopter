import pytest
import random
import itertools
from ev.universe import Universe

@pytest.fixture
def filename(tmpdir):
    return str(tmpdir.join('creatures.db'))

class FakeEnv(object):
    def run(self, c):
        return c.id

def test_first_generation(filename):
    uni = Universe(filename, envs=None, population=10)
    assert len(uni.alive) == 10
    ids = [c.id for c in uni.alive]
    assert sorted(ids) == range(1, 11)
    for c in uni.alive:
        assert uni.db.get_fitness(c) is None


def test_compute_fitness(filename):
    uni = Universe(filename, envs=[FakeEnv()], population=5)
    uni.compute_fitness()
    #
    for c in uni.alive:
        fitness = uni.db.get_fitness(c)
        assert fitness == c.id

def test_compute_fitness_partial(filename):
    uni = Universe(filename, envs=[FakeEnv()], population=5)
    creatures = list(uni.alive)
    creatures.sort(key=lambda c: c.id)
    c1, c2, c3, c4, c5 = creatures
    #
    # manually compute the fitness for c1 and c2
    uni.db.update_fitness(c1, 10)
    uni.db.update_fitness(c2, 20)
    #
    computed = set()
    def compute_fitness_one(c):
        computed.add(c)
        return 1
    uni.compute_fitness_one = compute_fitness_one
    uni.compute_fitness()
    assert computed == set([c3, c4, c5])


def test_kill_some(filename, monkeypatch):
    def my_sample(population, k):
        # not really random :)
        population = list(population)
        population.sort(key=lambda c: c.id)
        return population[:k]
    monkeypatch.setattr(random, 'sample', my_sample)
    #
    uni = Universe(filename, envs=[FakeEnv()], population=100)
    all_creatures = list(uni.alive)
    all_creatures.sort(key=lambda c: c.id)
    uni.compute_fitness() # c1 is the best, c100 is the worst
    uni.kill_some()
    #
    # check that the expected creatures survived
    all_ids = range(1, 101)
    best = all_ids[:10]
    unlucky = all_ids[10:15]
    good = all_ids[15:50] # (excluding the unlucky ones)
    lucky = all_ids[50:55]
    bad = all_ids[55:]    # (excluding the lucky ones)
    alive_ids = sorted([c.id for c in uni.alive])
    assert alive_ids == (best + good + lucky)
    #
    # check that the DB agrees about what is alive and what it's not
    for c in all_creatures:
        should_be_alive = (c in uni.alive)
        assert uni.db.is_alive(c) == should_be_alive
