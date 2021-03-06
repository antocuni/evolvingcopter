import pytest
import numpy as np
from ev.db import CreatureDB

@pytest.fixture
def db():
    return CreatureDB(":memory:")

class FakeCreature(object):

    def __init__(self, data):
        self.id = None
        self.data = data


class TestDB(object):

    def test_new_load(self, db):
        c1 = FakeCreature('hello')
        c2 = FakeCreature('world')
        db.new(c1)
        db.new(c2)
        assert c1.id == 1
        assert c2.id == 2
        #
        x1 = db.load(1)
        assert x1.id == 1
        assert x1.data == 'hello'
        #
        x2 = db.load(2)
        assert x2.id == 2
        assert x2.data == 'world'

    def test_update_fitness(self, db):
        c1 = FakeCreature('hello')
        c2 = FakeCreature('world')
        db.new(c1)
        db.new(c2)
        db.update_fitness(c1, 10)
        db.update_fitness(c2, 100)
        rows = db.load_all()
        assert rows == [
            (1, 0, None, 10),
            (2, 0, None, 100),
        ]

    def test_generation(self, db):
        c1 = FakeCreature('hello')
        c2 = FakeCreature('world')
        db.new(c1)
        db.new_generation()
        db.new(c2)
        rows = db.load_all()
        assert rows == [
            (1, 0, None, None), # generation 0
            (2, 1, None, None), # generation 1
        ]

    def test_kill(self, db):
        c1 = FakeCreature('hello')
        c2 = FakeCreature('world')
        db.new(c1)
        db.new(c2)
        assert db.is_alive(c1)
        assert db.is_alive(c2)
        db.kill(c2)
        assert db.is_alive(c1)
        assert not db.is_alive(c2)
