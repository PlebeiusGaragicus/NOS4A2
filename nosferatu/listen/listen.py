import os
import time
import json
import uuid
import ssl
import datetime
import websocket
import logging
from logging.handlers import QueueHandler
logger = None


from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import PrivateKey, PublicKey

from pymongo import MongoClient

from nosferatu.config import MONGODB_NAME


def init_listener(settings_json, queue, log_queue):
    queue_handler = QueueHandler(log_queue)
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(queue_handler)
    logger.info("Listener started for: %s", settings_json['name'])

    # client = MongoClient('localhost', 27017)
    # db = client[ MONGODB_NAME ]
    # collection = db['mycollection']

    # while True:
    #     dm = get_dm()
    #     inserted_document = collection.insert_one(dm)
    #     queue.put(inserted_document.inserted_id)


    while True:
        try:
            listen(settings_json, queue)
        except websocket._exceptions.WebSocketConnectionClosedException:
            logger.error("WebSocketConnectionClosedException")
            exit(1)

            # TODO - retry a number of times before giving up
            # time.sleep(5)
            # listen()

    




def listen(settings_json, queue):
    prv = settings_json['private_key']
    if prv in [None, ""]:
        logger.critical("private_key not set!")
        exit(1)

    prv = PrivateKey(bytes.fromhex(prv))
    pubkey = prv.public_key.hex()

    filters = Filters([Filter(pubkey_refs=[pubkey], kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE])])
    subscription_id = uuid.uuid1().hex
    relay_manager = RelayManager()

    relay_list = settings_json["relays"]
    if relay_list == {}:
        logger.critical("No relays added for bot!")
        exit(1)

    for r in relay_list:
        if r['read'] == True:
            relay_manager.add_relay(r['url'])

    relay_manager.add_subscription(subscription_id, filters)
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification

    request = [ClientMessageType.REQUEST, subscription_id]
    request.extend(filters.to_json_array())
    message = json.dumps(request)

    time.sleep(1.25) # allow the connections to open
    relay_manager.publish_message(message)
    time.sleep(1) # allow the messages to send


    while True:
        # TODO: check if the websocket closes.. and reopen if needed.
        # TODO: I should probably break this up into a few functions...
        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()

            from_pub = event_msg.event.public_key
            # name = hex_following[from_pub]['name'] # look up the name we gave this person

            msg = prv.decrypt_message(event_msg.event.content, from_pub)
            # logger.info(f"INBOX: from {from_pub}: {msg}")
            logger.info(f"NEW DM from {from_pub}:\n`{msg}`")
            queue.put(msg)
