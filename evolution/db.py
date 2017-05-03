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

    def count(self):
        self.cur.execute("SELECT COUNT(*) from creatures")
        return self.cur.fetchone()[0]

    def load_all(self):
        """
        Return all the data *except* the creature itself
        """
        self.cur.execute("SELECT id, born_at, killed_at, fitness FROM creatures")
        return self.cur.fetchall()

