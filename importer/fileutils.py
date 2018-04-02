import logging
import os

logger = logging.getLogger()

def findTxtFiles(rootPath, fileSuffix='.txt'):
    logger.debug('looking for txt files from %s', rootPath)
    for subdir, dirs, files in os.walk(rootPath):
        for file in files:
            filePath = subdir + os.sep + file
            if filePath.endswith(fileSuffix):
                logger.debug('found file %s', filePath)
