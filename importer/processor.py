import logging
from datamodel import DataModel
from datamodel import Row
import fileutils
import time
from collections import Counter

from nltk.stem.snowball import SnowballStemmer

logger = logging.getLogger()

def printDict(d):
    sortedKeys = sorted(d.keys())
    for key in sortedKeys:
        print(key, ' => ', d[key])

def formatForCSV(keywords, allCounters):
    sortedKeys = sorted(keywords)
    headerRow = 'filename,' + ','.join(sortedKeys) + '\n'

    valueRows = []

    sortedNames = sorted(allCounters.keys())
    for name in sortedNames:
        valueRow = formatRowForCSV(name, sortedKeys, allCounters[name])
        valueRows.append(valueRow)

    return headerRow  + '\n'.join(valueRows) + '\n'

def formatRowForCSV(name, keywords, counter):
    sortedKeys = sorted(keywords)
    sortedValues = []
    for key in sortedKeys:
        sortedValues.append(str(counter[key]))

    row = ','.join(sortedValues)
    return name + ',' + row

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
        rows = self.model.findByName(name)
        if (rows):
            all = dict()
            for row in rows:
                counter = self.processRow(row, self.keywords, self.noise)
                all[row.name] = counter

            printDict(all)
            csv = formatForCSV(self.keywords, all)
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
