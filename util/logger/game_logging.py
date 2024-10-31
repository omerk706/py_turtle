import logging

LOG_FORMAT = '%(asctime)s -%(levelname)s @ %(filename)s.%(funcName)s#%(lineno)d: %(message)s'


def setup_logging(log_file, level=logging.DEBUG):
    logging.basicConfig(filename=log_file, format=LOG_FORMAT, level=level)
    logging.info("logging configured")
