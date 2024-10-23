import logging

logger = logging.getLogger()
logHandler = logging.StreamHandler()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
