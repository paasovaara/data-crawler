import logging
import fileutils
from importer import Importer

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.info('Launching app')
    # TODO parse args: root folder

    i = Importer()
    i.launch('.')
