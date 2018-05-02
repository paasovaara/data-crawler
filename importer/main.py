import logging
import fileutils
import argparse

from importer import Importer
from processor import Processor
from datamodel import DataModel

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def startImport(root):
    i = Importer()
    i.launch(root)

def startProcess(name, language, keywordfile, noisefile):
    p = Processor(language, keywordfile, noisefile)
    p.process(name)

if __name__ == '__main__':
    logger.info('Launching app')

    parser = argparse.ArgumentParser(description='Import or process data')
    parser.add_argument('cmd', type=str, choices=['import', 'process', 'list'],
        help='Application mode')

    parser.add_argument('--root', type=str, default='.',
        help='root folder for the import. default is curdir')
    parser.add_argument('--name', type=str,
        help='name of the company to process, by default all is processed')
    parser.add_argument('--keywordfile', type=str, default='conf/keywords.txt',
        help='filename containing the keywords')
    parser.add_argument('--noisefile', type=str, default='conf/noise.txt',
        help='filename containing words considered as noise')
    parser.add_argument('--language', type=str, default='english',
        help='language for the stemmer. default=finnish')

    args = parser.parse_args()
    print(args.root)
    if (args.cmd == 'import'):
        logger.info('starting import from folder %s', args.root)
        startImport(args.root)
    elif(args.cmd == 'process'):
        if (args.name):
            logger.info('TODO start processing (name: %s) :)', args.name)
            startProcess(args.name, args.language, args.keywordfile, args.noisefile)
        else:
            logger.info('TODO Process ALL :)')
    elif(args.cmd == 'list'):
        model = DataModel()
        if (model.initialize()):
            items = model.list()
            logger.info('\n'.join(items))
