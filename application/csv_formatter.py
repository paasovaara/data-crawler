import re


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


def rowFormatForCSV(keywords, allCounters):
    sortedKeys = sorted(keywords)
    headerRow = 'filename,prefix,year,' + ','.join(sortedKeys) + '\n'
    valueRows = []

    sortedNames = sorted(allCounters.keys())
    for name in sortedNames:
        valueRow = _formatRowForCSV(name, sortedKeys, allCounters[name])
        valueRows.append(valueRow)

    return headerRow + '\n'.join(valueRows) + '\n'


def _formatRowForCSV(name, keywords, counter):
    sortedKeys = sorted(keywords)
    sortedValues = []
    for key in sortedKeys:
        sortedValues.append(str(counter[key]))

    #TODO refactor
    year = parseYearFromName(name)
    prefix = parsePrefixFromName(name)

    row = ','.join(sortedValues)
    return name + ',' + prefix + "," + year + "," + row


