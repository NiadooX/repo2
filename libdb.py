import sqlite3


class DB:
    print('dasdsadsa')
    def __init__(self, db_name):
        self.db = sqlite3.connect(f'{db_name}.db')
        self.cur = self.db.cursor()
