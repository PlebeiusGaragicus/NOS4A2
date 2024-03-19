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

from nosferatu_cli.config import MONGODB_NAME
from nosferatu_cli.keys import hexToNpub, hexToNpub


def init_listener(settings_json, queue, log_queue, keep_alive):
    queue_handler = QueueHandler(log_queue)
    global logger
    logger = logging.getLogger("listener")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(queue_handler)

    # TODO - validate settings_json

    while True:
        try:
            listen(settings_json, queue, keep_alive)
        except websocket._exceptions.WebSocketConnectionClosedException:
            logger.error("WebSocketConnectionClosedException")
            exit(1)
        
        if not keep_alive:
            break

            # TODO - retry a number of times before giving up
            # time.sleep(5)
            # listen()

    




def listen(settings_json, queue, keep_alive):
    client = MongoClient('localhost', 27017)
    db = client[ MONGODB_NAME ]
    collection_name = settings_json['name']
    collection = db[ collection_name ]

    # while True:
    #     dm = get_dm()
    #     inserted_document = collection.insert_one(dm)
    #     queue.put(inserted_document.inserted_id)



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

            name = f"npub...{from_pub[-8:]}"
            for f in settings_json['following']:
                if f['npub'] == hexToNpub(from_pub):
                    name = f['name']
                    break

            clear_text = prv.decrypt_message(event_msg.event.content, from_pub)
            event_msg.event.content = clear_text

            logger.info(f"NEW DM from {name}:\n`{clear_text}`")
            # print(event_msg.event.__dict__)

            # TODO do I need to confirm the signature?
            new_database_entry = {
                "id": event_msg.event.id,
                "kind": "ENCRYPTED_DIRECT_MESSAGE",
                "created_at": event_msg.event.created_at,
                "clear_text": clear_text,
                "pubkey": from_pub,
                "tags": event_msg.event.tags,
                "relay": event_msg.url,
            }

            # ensure the event is unique in the database
            if collection.count_documents({"id": event_msg.event.id}) == 0:
                collection.insert_one( new_database_entry )
                queue.put({
                    "pubkey": from_pub,
                    "message": clear_text,
                    "relay": event_msg.url,
                    "event_id": event_msg.event.id,
                })
            else:
                logger.warning(f"Duplicate event: {event_msg.event.id}")

        if not keep_alive:
            relay_manager.close_connections()
            time.sleep(0.5)
            break

# event
# {
# 'event': <nostr.event.Event object at 0x1024c1430>,
# 'subscription_id': '10a0a1fee5a111ee9a0386a48980b0e6',
# 'url': 'wss://relay.damus.io'
# }

# event.event
# {
# 'public_key': 'a6b218b1d6fed97636bb9d855959bf84551a2a20d4795c452950457d9f62ecd0',
# 'content': 'd4T4Ab6t2q46mp4mOx6yGQ==?iv=h4Oql2NwLeqyWGQEACimHw==',
# 'created_at': 1710354155,
# 'kind': 4,
# 'tags': [['p', '425f31625bd7114a3925019153a8aa8fb23375efd8b780882d7ebaf51bf63e8c']],
# 'signature': 'e39badd35ce8bd25d8fbb27c7d05f8826abdfac893b811722f4acb9d524a5365211919b9e35edc4decc2befd8dcf83f98884ecd5e8f95546dcb0385ee58cfdef',
# 'id': '45ca487cba654b76503039345ac1ef7368b11af1dac0764a805002111b3d6ecd'
# }
