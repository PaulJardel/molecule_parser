from molecular.monitoring.log import get_logger

logger = get_logger()

USERNAME = "Paul"
tag_dict = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5
}


def hello():

    logger.info(f'Hello {USERNAME}')


if __name__ == '__main__':
    hello()
