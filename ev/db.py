import sqlite3
import cPickle as pickle

class CreatureDB(object):

    def __init__(self, filename):
        self.conn = sqlite3.connect(filename, isolation_level=None) # autocommit
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS creatures (
                id INTEGER PRIMARY KEY,
                born_at INTEGER,
                killed_at INTEGER,
                fitness REAL,
                pickled TEXT
            )
        """)
        self.cur.execute("SELECT MAX(born_at) FROM creatures")
        self.generation = self.cur.fetchone()[0]
        if self.generation is None:
            self.generation = 0

    @property
    def atomic(self):
        return Transaction(self.cur)

    def new_generation(self):
        self.generation += 1

    def new(self, c):
        """
        Insert a new creature in the DB, and set c.id accordingly
        """
        assert c.id is None
        # create a new row in the DB, to generate an ID
        self.cur.execute("INSERT INTO creatures(id) VALUES(NULL)")
        c.id = self.cur.lastrowid
        born_at = self.generation
        pickled = pickle.dumps(c)
        # save the updated c
        self.cur.execute("""
            UPDATE creatures
            SET born_at = ?, pickled = ?
            WHERE id = ?
        """, (born_at, pickled, c.id))

    def load(self, id):
        self.cur.execute("SELECT pickled FROM creatures WHERE id=?", (id,))
        pickled = self.cur.fetchone()[0]
        return pickle.loads(pickled)

    def update_fitness(self, c, fitness):
        assert c.id is not None
        self.cur.execute("""
            UPDATE creatures
            SET fitness = ?
            WHERE id = ?
        """, (fitness, c.id))

    def get_fitness(self, c):
        assert c.id is not None
        self.cur.execute("SELECT fitness FROM creatures WHERE id=?", (c.id,))
        fitness = self.cur.fetchone()[0]
        return fitness

    def kill(self, c):
        assert c.id is not None
        killed_at = self.generation
        self.cur.execute("""
            UPDATE creatures
            SET killed_at = ?
            WHERE id = ?
        """, (killed_at, c.id))

    def is_alive(self, c):
        assert c.id is not None
        self.cur.execute("SELECT killed_at FROM creatures WHERE id=?", (c.id,))
        killed_at = self.cur.fetchone()[0]
        return killed_at is None

    def count(self):
        self.cur.execute("SELECT COUNT(*) FROM creatures")
        return self.cur.fetchone()[0]

    def load_all(self):
        """
        Return all the data *except* the creature itself
        """
        self.cur.execute("SELECT id, born_at, killed_at, fitness FROM creatures")
        return self.cur.fetchall()

    def load_best(self):
        """
        Return the best creature ever recorded
        """
        self.cur.execute("""
            SELECT id
            FROM creatures
            WHERE fitness == (
                SELECT MIN(fitness) FROM creatures
            )
        """)
        id = self.cur.fetchone()[0]
        return self.load(id)

class Transaction(object):

    def __init__(self, cur):
        self.cur = cur

    def __enter__(self):
        self.cur.execute('BEGIN')
        return self

    def __exit__(self, etype, evalue, tb):
        if etype:
            self.cur.execute('ROLLBACK')
        else:
            self.cur.execute('COMMIT')
