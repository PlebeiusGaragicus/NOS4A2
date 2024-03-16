import logging
logger = logging.getLogger("nospy")

from pymongo import MongoClient


def send_response(response, sender):
    logger.debug(f"Sending response to {sender}: {response}")

# Sender process
def sender(response_queue):
    logger.error("sender() not yet implemented")
    exit(1)

    while True:
        if not response_queue.empty():
            response = response_queue.get()
            sender = get_sender()
            send_response(response, sender)
