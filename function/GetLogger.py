import inspect
import logging


def configure_logging():
    format = "%(asctime)s :%(levelname)s : %(name)s :%(message)s"
    logging.basicConfig(filemode='w', filename='logfile.log', encoding='utf-8', level=logging.DEBUG, format=format,
                        datefmt='%d/%m/%y %H:%M:%S')


def get_logger():

    loggerName = inspect.stack()[1][3]
    logger = logging.getLogger(loggerName)

    file_handler = logging.FileHandler('logfile.log', mode='w')
    # fileHandler = logging.FileHandler('{0}.format(logName), mode='a')

    formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s", datefmt='%d/%m/%y %H:%M:%S')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)  # filehandler object
    logger.setLevel(logging.DEBUG)

    return logger

def test_logger():
    logger = get_logger()

    logger.critical('This is critical message')
    logger.error('Tis is an error msg')
    logger.warning('This is a warning msg')
    logger.info('This is an info msg')
    logger.debug('This is a debug message')