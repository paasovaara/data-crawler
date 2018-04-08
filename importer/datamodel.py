import logging
import sqlite3

logger = logging.getLogger()
DB_NAME="data.db"

class DataModel(object):

    def initialize(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute('SELECT name FROM sqlite_master WHERE type=\'table\';')
        result = c.fetchall()
        if (len(result) == 0):
            self.createDb()
        else:
            logger.info('Database initialized OK')


    def createDb(self):
        logger.warn('Creating the database tables')
