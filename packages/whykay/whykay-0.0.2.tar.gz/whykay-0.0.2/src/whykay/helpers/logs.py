import sys
import logging

def init_logger(name):
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger = logging.getLogger(name)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    return logger
