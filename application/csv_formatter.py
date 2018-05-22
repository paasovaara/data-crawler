import re
from itertools import groupby
import logging


_logger = logging.getLogger()


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


# TODO refactor this. now tries to parse a year from the filename
# think how to do this modulary, add decorators etc.?
def _parseDataFromName(name):
    year = parseYearFromName(name)
    prefix = parsePrefixFromName(name)
    return name, prefix, year


def rowFormatForCSV(keywords, allCounters):
    sortedKeys = sorted(keywords)
    headerRow = 'filename,prefix,year,' + ','.join(sortedKeys) + '\n'
    valueRows = []

    sortedNames = sorted(allCounters.keys())
    for name in sortedNames:
        valueRow = _formatSimpleRowForCSV(name, sortedKeys, allCounters[name])
        valueRows.append(valueRow)

    return headerRow + '\n'.join(valueRows) + '\n'


def _formatSimpleRowForCSV(name, keywords, counter):
    sortedKeys = sorted(keywords)
    sortedValues = []
    for key in sortedKeys:
        sortedValues.append(str(counter[key]))

    metadata = _parseDataFromName(name)
    prefix = metadata[1]
    year = metadata[2]
    row = ','.join(sortedValues)
    return name + ',' + prefix + "," + year + "," + row


 # def _formatAllDataToSingleRowForCSV(prefix, allDataForPrefix, keywords, allCounters):
 #     sortedKeys = sorted(keywords)
 #     sortedValues = []
 #     for key in sortedKeys:
 #         for year in allDataForPrefix
 #         sortedValues.append(str(counter[key]))
 #
 #     metadata = _parseDataFromName(name)
 #     prefix = metadata[1]
 #     year = metadata[2]
 #     row = ','.join(sortedValues)
 #     return name + ',' + prefix + "," + year + "," + row


_YEARS_PER_KEYWORD = 10


def colFormatForCSV(keywords, allCounters):

    sortedKeys = sorted(keywords)
    # This is a very specific case. TODO generalize somehow
    colYears = sorted(range(2017 - _YEARS_PER_KEYWORD + 1, 2018), reverse=True)
    colHeaders = []
    for key in sortedKeys:
        for colYear in colYears:
            colHeaders.append(key + ' ' + str(colYear))

    #sortedNames = sorted(allCounters.keys())
    #for name in sortedNames:
    #    valueRow = _formatRowForCSV(name, sortedKeys, allCounters[name])
    #    valueRows.append(valueRow)

    headerRow = 'prefix,' + ','.join(colHeaders) + '\n'
    #valueRows = []

    # first pre-process/augment the data
    keysWithPrefixAndYear = map(_parseDataFromName, allCounters.keys())
    sortedKeysWithPrefixAndYear = sorted(keysWithPrefixAndYear, key=lambda x: x[1])

    dataRows = []
    for key, group in groupby(sortedKeysWithPrefixAndYear, key=lambda x: x[1]):
        _logger.info('key %s has these entries: ', key)
        sortedData = sorted(group, key=lambda x: x[2], reverse=True)

        dataRow = []
        dataRow.append(key)
        for keyWord in sortedKeys:

            # sort by year, latest first
            index = 0
            # This has a bug, in case some entry has less than 10 years of data.

            for data in sortedData:
                index += 1
                if index <= _YEARS_PER_KEYWORD:
                    _logger.info('%s, source data %s: prefix %s, year %s ', keyWord, data[0], data[1], data[2])
                    filename = data[0]
                    counter = allCounters[filename]
                    count = str(counter[keyWord])
                    dataRow.append(count)

        dataRows.append(','.join(dataRow))


    return headerRow + '\n'.join(dataRows) + '\n'
    #return headerRow + '\n'.join(valueRows) + '\n'


