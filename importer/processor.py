import logging
from datamodel import DataModel
from datamodel import Row
import fileutils

logger = logging.getLogger()

class Processor(object):
    model = DataModel()

    def process(self, name):

        for test in fileutils.safeReadWordsFromFile('conf/keywords.txt'):
            logger.info(test)

        logger.info('processing %s', name)
        row = self.model.findByName(name)
        if (row):
            logger.info('row: %s', row.data)
        else:
            logger.error('no data for name %s', name)


    #def readKeywords(filename):
