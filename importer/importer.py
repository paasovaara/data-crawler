import logging
import fileutils
import io

logger = logging.getLogger()

class Importer(object):

    #def __init__(self):

    def launch(self, rootFolder):
        files = fileutils.findFiles(rootFolder,'.py')
        for filedata in files:
            logger.info(str(filedata))

        self.importFiles(files)

    def importFiles(self, files):
        logger.info("importing %s files", len(files))
        for file in files:
            with open(file.path,'r') as f:
                data = f.read()
                logger.info(data)
