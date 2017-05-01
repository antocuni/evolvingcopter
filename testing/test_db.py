import pytest
import numpy as np
from evolution.db import CreatureDB

@pytest.fixture
def db():
    return CreatureDB(":memory:")

class FakeCreature(object):

    def __init__(self, generation, data):
        self.id = None
        self.generation = generation
        self.data = data


class TestDB(object):

    def test_save_load(self, db):
        c1 = FakeCreature(42, 'hello')
        c2 = FakeCreature(43, 'world')
        db.save(c1)
        db.save(c2)
        assert c1.id == 1
        assert c2.id == 2
        #
        x1 = db.load(1)
        assert x1.id == 1
        assert x1.generation == 42
        assert x1.data == 'hello'
        #
        x2 = db.load(2)
        assert x2.id == 2
        assert x2.generation == 43
        assert x2.data == 'world'
