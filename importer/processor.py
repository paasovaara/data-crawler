import logging
from datamodel import DataModel
from datamodel import Row

logger = logging.getLogger()

class Processor(object):
    model = DataModel()

    def process(self, name):
        logger.info('processing %s', name)
        row = self.model.findByName(name)
        logger.info('row: %s', row.data)
        
