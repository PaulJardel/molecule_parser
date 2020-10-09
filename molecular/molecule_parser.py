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
    logger.info(f'len(character) = {len(USERNAME)}')
    index_end = len(USERNAME)
    for index, character in enumerate(USERNAME):
        logger.info(f'index {index}')
        if index < index_end:
            index_next_char = index+1
        else:
            index_next_char = index_end-1
        logger.info(f'index_next_char {index_next_char}')
        logger.info(f'character = {index} {character}')


if __name__ == '__main__':
    hello()
