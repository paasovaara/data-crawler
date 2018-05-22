import logging
import fileutils
from models.datamodel import DataModel
from models.datamodel import TextDataRow

logger = logging.getLogger()


class Importer(object):
    model = DataModel()

    def launch(self, rootFolder):
        if not self.model.initialize():
            return

        files = fileutils.findFiles(rootFolder,'.txt')
        for filedata in files:
            logger.info(str(filedata))

        logger.info('inserting %s files to database', str(len(files)))
        self.importFiles(files)
        logger.info('Database contains %s files', str(self.model.count()))

    def importFiles(self, files):
        logger.info("importing %s files", len(files))
        for file in files:
            with open(file.path,'r') as f:
                data = f.read()
                #logger.info(data)
                row = TextDataRow(file.name, file.path, data)
                #self.insert(temp)
                if self.model.insert(row):
                    logger.info('file %s inserted successfully', file.path)
                else:
                    logger.error('file %s FAILED to insert', file.path)
