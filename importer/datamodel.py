import logging
import sqlite3

logger = logging.getLogger()
DB_NAME="data.db"


# TODO create separate SQL script
CREATE_TABLE="""CREATE TABLE TextData(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(255),
    filepath VARCHAR(255),
    data TEXT
);"""

class Row(object):
    __slots__ = 'id', 'created', 'name', 'filepath', 'data'

    def __init__(self, name, filepath, data):
        self.name= name
        self.filepath = filepath
        self.data = data

class DataModel(object):
    conn = None
    c = None

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.c = self.conn.cursor()

    def doesDbExist(self):
        self.c.execute('SELECT name FROM sqlite_master WHERE type=\'table\';')
        result = self.c.fetchall()
        return (len(result) > 0)

    def initialize(self):
        self.c.execute('SELECT name FROM sqlite_master WHERE type=\'table\';')
        result = self.c.fetchall()
        if (not self.doesDbExist()):
            if (not self.createDb()):
                logger.error('FAILED TO CREATE DATABASE')

        else:
            logger.info('Database initialized OK')
            logger.info('Database rowcount: %s', self.count())
            #temp = Row("myname", "myfilepath", "this is the content")
            #self.insert(temp)


    def createDb(self):
        logger.warn('Creating the database tables')
        self.c.execute(CREATE_TABLE)
        self.conn.commit()
        return self.doesDbExist()

    def count(self):
        self.c.execute('SELECT COUNT(id) FROM TextData;')
        result = self.c.fetchone()[0]
        return result

    def insert(self, row):
        try:
            data = (row.name, row.filepath, row.data)
            self.c.execute('INSERT INTO TextData (name, filepath, data) VALUES (?, ?, ?);', data)
            self.conn.commit()

        except Exception as err:
            logger.error('Insert Failed, Error: %s', str(err))
