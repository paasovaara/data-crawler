import logging
from datamodel import DataModel
from datamodel import Row
import fileutils

from nltk.stem.snowball import SnowballStemmer

logger = logging.getLogger()

class Processor(object):

    __slots__ = 'model', 'language', 'stemmer', 'keywords', 'noise'

    def __init__(self, language, keywordfile, noisefile):
        self.model = DataModel()
        self.language = language
        self.stemmer = SnowballStemmer(language)
        logger.info('creating stemmer for language %s', language)
        self.keywords = fileutils.safeReadWordsFromFile(keywordfile)
        for key in self.keywords:
            logger.debug(key)
            self.prepare(key)

        self.noise = fileutils.safeReadWordsFromFile(noisefile)
        for key in self.noise:
            logger.debug(key)
            self.prepare(key)


    def prepare(self, word):
        logger.info(word + ' => ' + self.stemmer.stem(word))

    def process(self, name):
        logger.info('processing %s', name)
        row = self.model.findByName(name)
        if (row):
            self.processRow(row, self.keywords, self.noise)
        else:
            logger.error('no data for name %s', name)

        #TODO Next:
        #- MVP: just calculate the words from file.
        #- then apply  stemming and lemming and allthat

        # For merging (prod ready)
        #- add app argument to specify the keyword and noise file

    def processRow(self, row, keywords, noise):
        logger.debug('processing row: %s', row.name)
