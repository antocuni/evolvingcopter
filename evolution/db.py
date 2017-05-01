import sqlite3
import cPickle as pickle

class CreatureDB(object):

    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS creatures (
                id INTEGER PRIMARY KEY,
                generation INTEGER,
                fitness REAL,
                pickled TEXT
            )
        """)

    def save(self, c):
        """
        Insert a new creature in the DB, and set c.id accordingly
        """
        assert c.id is None
        # create a new row in the DB, to generate an ID
        self.cur.execute("INSERT INTO creatures(id) VALUES(NULL)")
        c.id = self.cur.lastrowid
        pickled = pickle.dumps(c)
        # save the updated c
        self.cur.execute("""
            UPDATE creatures
            SET generation = ?, pickled = ?
            WHERE id = ?
        """, (c.generation, pickled, c.id))

    def load(self, id):
        self.cur.execute("SELECT pickled FROM creatures WHERE id=?", (id,))
        pickled = self.cur.fetchone()[0]
        return pickle.loads(pickled)
