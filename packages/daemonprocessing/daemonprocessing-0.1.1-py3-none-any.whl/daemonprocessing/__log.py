import logging

log_file = f'{__package__}.log'

logger = logging.getLogger(__package__)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logger.addHandler(stream_handler)
logger.setLevel(logging.NOTSET)