import logging
from datamodel import DataModel
from datamodel import Row
import fileutils

logger = logging.getLogger()

class Processor(object):
    model = DataModel()

    def process(self, name):
        keywords = fileutils.safeReadWordsFromFile('conf/keywords.txt')
        for key in keywords:
            logger.debug(key)

        noise = fileutils.safeReadWordsFromFile('conf/noise.txt')
        for key in noise:
            logger.debug(key)

        logger.info('processing %s', name)
        row = self.model.findByName(name)
        if (row):
            logger.info('row: %s', row.data)
        else:
            logger.error('no data for name %s', name)

        #TODO Next:
        #- MVP: just calculate the words from file.
        #- then apply  stemming and lemming and allthat

        # For merging (prod ready)
        #- add app argument to specify the keyword and noise file
