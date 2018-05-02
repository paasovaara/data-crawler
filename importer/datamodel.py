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

    def __repr__(self):
        return '[' + str(self.id) + '] name: ' + self.name + ' (from:' + self.filepath + ') with content: ' + self.data


def rowFromResult(result):
    if result == None:
        return None
    row = Row(result[2], result[3], result[4])
    row.id = result[0]
    row.created = result[1]
    #logger.info(str(row))
    return row


class DataModel(object):
    conn = None
    cursor = None

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

    def doesDbExist(self):
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\';')
        result = self.cursor.fetchall()
        return (len(result) > 0)

    def initialize(self):
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\';')
        result = self.cursor.fetchall()
        if (not self.doesDbExist()):
            if (not self.createDb()):
                logger.error('FAILED TO CREATE DATABASE')
                return False
            else:
                return True
        else:
            logger.info('Database initialized OK')
            logger.info('Database rowcount: %s', self.count())
            return True


    def createDb(self):
        logger.warn('Creating the database tables')
        self.cursor.execute(CREATE_TABLE)
        self.conn.commit()
        return self.doesDbExist()

    def count(self):
        self.cursor.execute('SELECT COUNT(id) FROM TextData;')
        result = self.cursor.fetchone()[0]
        return result

    def insert(self, row):
        try:
            data = (row.name, row.filepath, row.data)
            self.cursor.execute('INSERT INTO TextData (name, filepath, data) VALUES (?, ?, ?);', data)
            self.conn.commit()
            return True
        except Exception as err:
            logger.error('Insert Failed, Error: %s', str(err))
            return False

    def findByName(self, name):
        query = '%' + name.lower() + '%'
        self.cursor.execute('SELECT * FROM TextData WHERE LOWER(name) LIKE ? ORDER BY name DESC;', (query,))
        result = self.cursor.fetchone()
        return rowFromResult(result)
