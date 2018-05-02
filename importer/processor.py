import logging
from datamodel import DataModel
from datamodel import Row
import fileutils
import time
from collections import Counter

from nltk.stem.snowball import SnowballStemmer

logger = logging.getLogger()

class Processor(object):

    __slots__ = 'model', 'language', 'stemmer', 'keywords', 'noise'

    def __init__(self, language, keywordfile, noisefile):
        self.model = DataModel()
        self.language = language
        self.stemmer = SnowballStemmer(language)
        logger.info('creating stemmer for language %s', language)
        self.keywords = self.prepareWords(keywordfile)
        self.noise = self.prepareWords(noisefile)

    def prepareWords(self, file):
        words = fileutils.safeReadWordsFromFile(file)
        wordSet = set()
        for w in words:
            prepared = self.prepare(w)
            logger.info(w + ' => ' + prepared)
            wordSet.add(prepared)
        return wordSet

    def prepare(self, word):
        return self.stemmer.stem(word.strip().lower())


    def process(self, name):
        logger.info('processing %s', name)
        row = self.model.findByName(name)
        if (row):
            self.processRow(row, self.keywords, self.noise)
        else:
            logger.error('no data for name %s', name)

    def processRow(self, row, keywords, noise):
        logger.debug('processing row: %s', row.name)
        start = time.time()

        content = row.data.split('\n')
        words = fileutils.splitLinesIntoWords(content)
        logger.debug('word count in document: %d', len(words))

        counter = Counter()
        for word in words:
            wordLc = self.prepare(word)
            if (not wordLc in noise and wordLc in keywords):
                counter[wordLc] += 1

        end = time.time()
        elapsed = end - start

        logger.debug('row %s processed in %.2f seconds', row.name, elapsed)
        logger.info(str(counter))
        #logger.debug(row.data)
