import ssl
import time
import json
import logging
from logging.handlers import QueueHandler
logger = None

from nostr.relay_manager import RelayManager
from nostr.event import EncryptedDirectMessage
from nostr.key import PrivateKey


from pymongo import MongoClient

# from nosferatu_cli.db import MONGODB_NAME
MONGODB_NAME = 'nosferatu'


def setup_logging(log_queue):
    queue_handler = QueueHandler(log_queue)
    global logger
    logger = logging.getLogger("replyer")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(queue_handler)



def init_sender(settings_json, response_queue, log_queue):
    setup_logging(log_queue)
    logger.info("Sender started for %s", settings_json['name'])

    key = settings_json['private_key'] # TODO - validate this
    private_key = PrivateKey( bytes.fromhex(key) )

    # client = MongoClient('localhost', 27017)
    # db = client[ MONGODB_NAME ]
    # collection_name = settings_json['name']

    relay_manager = RelayManager()

    relays = settings_json['relays']
    for r in relays:
        if r['write'] == True:
            relay_manager.add_relay(r['url'])

    # relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification

    # TODO - catch connection errors
    while True:
        if not response_queue.empty():
            relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
            time.sleep(0.5)

            response = response_queue.get()
            logger.info(f"Replying with:\n{response['content']}")

            # event = Event(public_key=settings_json['private_key'],
            #               content=response.content,
            #             #   created_at=None, # will be computed
            #               kind=EventKind.ENCRYPTED_DIRECT_MESSAGE,
            #               tags=[],
            #             #   id=None, # will be computed
            #               signature=None,
            #         )
            # event.id = event.compute_id()
            # event.sign(settings_json['private_key'])
            dm = EncryptedDirectMessage(
                    recipient_pubkey=response['pubkey'],
                    cleartext_content="this is a reply!!",
                    reference_event_id=response['event_id']
                )

            private_key.sign_event(dm)
            relay_manager.publish_event( dm )
            time.sleep(0.8) # allow the messages to send
            relay_manager.close_connections()
