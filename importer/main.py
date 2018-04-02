import logging
import fileutils

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.info('Launching app')
    files = fileutils.findFiles('.','.py')
    for filedata in files:
        logger.info(str(filedata))
