import pytest
from evolution.universe import Universe

@pytest.fixture
def filename(tmpdir):
    return str(tmpdir.join('creatures.db'))


def test_first_generation(filename):
    uni = Universe(filename, population=10)
    assert len(uni.alive) == 10
    ids = [c.id for c in uni.alive]
    assert sorted(ids) == range(1, 11)
    for c in uni.alive:
        assert uni.db.get_fitness(c) is None
