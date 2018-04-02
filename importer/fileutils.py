import logging
import os

logger = logging.getLogger()

class FileMetadata(object):
    __slots__ = 'path', 'name'

    def __init__(self):
        self.path = None
        self.name = None

    def __repr__(self):
        return 'my path is: ' + self.path


def findFiles(rootPath, fileSuffix='.txt'):
    logger.debug('looking for %s files from %s', fileSuffix, rootPath)
    list = []
    for subdir, dirs, files in os.walk(rootPath):
        for file in files:
            filePath = subdir + os.sep + file
            if filePath.endswith(fileSuffix):
                logger.debug('found file %s', filePath)
                data = FileMetadata()
                data.name = file
                data.path = filePath
                list.append(data)
    return list
