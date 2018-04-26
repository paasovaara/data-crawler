import logging
import fileutils
import argparse

from importer import Importer
from processor import Processor

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

def startProcess(name):
    p = Processor()
    p.process(name)

if __name__ == '__main__':
    logger.info('Launching app')

    parser = argparse.ArgumentParser(description='Import or process data')
    parser.add_argument('cmd', type=str, choices=['import', 'process'],
        help='Application mode')

    parser.add_argument('--root', type=str, default='.',
        help='root folder for the import. default is curdir')
    parser.add_argument('--name', type=str,
        help='name of the company to process, by default all is processed')

    args = parser.parse_args()
    print(args.root)
    if (args.cmd == 'import'):
        logger.info('starting import from folder %s', args.root)
        startImport(args.root)
    elif(args.cmd == 'process'):
        if (args.name):
            logger.info('TODO start processing (name: %s) :)', args.name)
            startProcess(args.name)
        else:
            logger.info('TODO Process ALL :)')
