import os
import time
import json
import uuid
import ssl
import datetime
import logging

from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import PrivateKey, PublicKey


from pymongo import MongoClient



from nosferatu.common import cprint, Colors


def get_dm():
    # return "Hello, World!"
    return input("Enter a direct message: ")


# Listener process
def listener(queue):
    client = MongoClient('localhost', 27017)
    db = client['mydatabase']
    collection = db['mycollection']

    # while True:
    #     dm = get_dm()
    #     inserted_document = collection.insert_one(dm)
    #     queue.put(inserted_document.inserted_id)

    prv = os.getenv("NOSFATTY_PRV_HEX")
    if prv in [None, ""]:
        cprint("NOSFATTY_PRV_HEX not set", Colors.RED)
        exit(1)

    prv = PrivateKey(bytes.fromhex(prv))
    pubkey = prv.public_key.hex()

    # create a filter to listen for direct messages to our public key
    filters = Filters([Filter(pubkey_refs=[pubkey], kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE])])

    # create a unique subscription id # TODO - I don't know what for yet
    subscription_id = uuid.uuid1().hex

    # create a relay manager and add our relays
    relay_manager = RelayManager()

    relays = st.session_state.settings["relays"]
    if relays == {}:
        cprint("You need to add a relay to run 'home'", Colors.RED)
        exit(1)

    for r in relays:
        if r['read'] == True:
            relay_manager.add_relay(r['url'])

    relay_manager.add_subscription(subscription_id, filters)
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification

    # create a request message to send to the relay
    request = [ClientMessageType.REQUEST, subscription_id]
    request.extend(filters.to_json_array())
    message = json.dumps(request)

    # send the request to the relay
    time.sleep(1.25) # allow the connections to open
    relay_manager.publish_message(message) # send the request to the relay
    time.sleep(1) # allow the messages to send


    while True:
        # TODO: check if the websocket closes.. and reopen if needed.
        # TODO: I should probably break this up into a few functions...
        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()

            from_pub = event_msg.event.public_key
            # name = hex_following[from_pub]['name'] # look up the name we gave this person

            # st.write(event_msg.event.created_at)
            msg = prv.decrypt_message(event_msg.event.content, from_pub)
            cprint(msg, Colors.BLUE)
