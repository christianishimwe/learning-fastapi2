
from contextlib import contextmanager


class Database:
    def __init__(self):
        # make connection to the database
        # self.conn =
        # get the cursor
        # self.cursor = self.conn.cursor()
        pass

    def __enter__(self):
        # mae a connection here
        return self
        pass

    def __exit__(self):
        # close the connection here
        pass


@contextmanager
def managed_database():
    db = Database()
    # connect to the database here
    yield db
    db.close()
