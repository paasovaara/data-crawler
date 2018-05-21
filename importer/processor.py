import logging
from models.datamodel import DataModel
from models.datamodel import TextDataRow
import fileutils
import time
from collections import Counter
import re

from nltk.stem.snowball import SnowballStemmer

logger = logging.getLogger()


def printDict(d):
    sortedKeys = sorted(d.keys())
    for key in sortedKeys:
        print(key, ' => ', d[key])


# TODO refactor this. now tries to parse a year from the filename
# think how to do this modulary, add decorators etc.?
def parseYearFromName(name):
    p = re.compile(r'\d{4}')
    m = p.search(name)
    #logger.info(m)
    if m:
        return m.group()
    else:
        return ''


def parsePrefixFromName(name):
    prefix = name.split('_',1)[0]
    if prefix:
        return prefix
    else:
        return ''


def formatForCSV(keywords, allCounters):
    sortedKeys = sorted(keywords)
    headerRow = 'filename,prefix,year,' + ','.join(sortedKeys) + '\n'
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

    #TODO refactor
    year = parseYearFromName(name)
    prefix = parsePrefixFromName(name)

    row = ','.join(sortedValues)
    return name + ',' + prefix + "," + year + "," + row


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
