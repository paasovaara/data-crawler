import logging
from models.datamodel import DataModel
from models.datamodel import TextDataRow
import fileutils
import time
import csv_formatter
from collections import Counter
from enum import Enum

from nltk.stem.snowball import SnowballStemmer

logger = logging.getLogger()


class ProcessMode(Enum):
    ROW = 1
    COL = 2


def printDict(d):
    sortedKeys = sorted(d.keys())
    for key in sortedKeys:
        print(key, ' => ', d[key])


def formatForCSV(keywords, allCounters, mode):
    if mode == ProcessMode.ROW:
        return csv_formatter.rowFormatForCSV(keywords, allCounters)
    else:
        return ''


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

    def process(self, name, mode=ProcessMode.ROW):
        logger.info('processing %s', name)
        rows = self.model.findByName(name)
        if rows:
            results = dict()
            for row in rows:
                counter = self.processRow(row, self.keywords, self.noise)
                results[row.name] = counter

            printDict(results)
            csv = formatForCSV(self.keywords, results, mode)
            fileutils.writeToFile(name + '.csv', csv)
        else:
            logger.error('no data for name %s', name)

    def processRow(self, row, keywords, noise):
        #logger.debug('processing row: %s', row.name)
        start = time.time()

        content = row.data.split('\n')
        words = fileutils.splitLinesIntoWords(content)
        #logger.debug('word count in document: %d', len(words))

        counter = Counter()
        for word in words:
            wordLc = self.prepare(word)
            if (not wordLc in noise and wordLc in keywords):
                counter[wordLc] += 1

        end = time.time()
        elapsed = end - start

        logger.debug('row %s processed in %.2f seconds', row.name, elapsed)
        #logger.info(str(counter))
        return counter
        #logger.debug(row.data)
