import logging

# Logger config
logger = logging.getLogger()

formatter = logging.Formatter('%(levelname)s | dsm-to-dtm | %(asctime)s | %(pathname)s | line %(lineno)d | %(message)s')

logger.setLevel(logging.INFO)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)