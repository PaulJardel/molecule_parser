import logging

DEFAULT_LEVEL = logging.INFO
PROJECT_NAME = "MOLECULE_PARSER"


def get_logger(level=DEFAULT_LEVEL):
    """
    Returns the logger for MOLECULE_PARSER project.

    - format the logger with date
    Example :
    logging.info('an info messge')
    2017-05-25 00:58:28 INFO     an info messge

    :param level : the level to use for the logger
    :return: the logger for MOLECULE_PARSER project
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(PROJECT_NAME)

    return logger
