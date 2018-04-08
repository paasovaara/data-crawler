import logging
import sqlite3

logger = logging.getLogger()
DB_NAME="data.db"


# TODO create separate SQL script
CREATE_TABLE="""CREATE TABLE TextData(
    id UNSIGNED BIG INT PRIMARY KEY NOT NULL,
    created INT NOT NULL,
    name VARCHAR(255),
    filepath VARCHAR(255),
    data TEXT
);"""

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


    def createDb(self):
        logger.warn('Creating the database tables')
        self.c.execute(CREATE_TABLE)
        self.conn.commit()
        return self.doesDbExist()
