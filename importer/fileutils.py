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
                #logger.debug('found file %s', filePath)
                data = FileMetadata()
                data.name = file
                data.path = filePath
                list.append(data)
    return list


def readWordsFromFile(filename):
    logger.debug('reading files from %s', filename)
    with open(filename) as file:
        lines = file.readlines()
        # ARGH, WHY DOES NOT FLATMAP EXIST!??
        words = []
        for line in lines:
            for word in line.split(' '):
                words.append(word.strip())
        return list(filter(lambda w: w != "", words))

def safeReadWordsFromFile(filename):
    try:
        return readWordsFromFile(filename)
    except OSError as e:
        logger.error('cannot read file %s, reason: %s', filename, e.strerror)
        return []
