import time
import logging
from logging.handlers import QueueHandler
logger = None

from pymongo import MongoClient


def setup_logging(log_queue):
    queue_handler = QueueHandler(log_queue)
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(queue_handler)



def init_sender(settings_json, response_queue, log_queue):
    setup_logging(log_queue)
    logger.info("Sender started for %s", settings_json['name'])



    while True:
        if not response_queue.empty():
            response = response_queue.get()
            logger.info(f"Replying with:\n{response}")
