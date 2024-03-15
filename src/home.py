import os
import time
import datetime
import json
import uuid
import ssl

import streamlit as st

from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import PublicKey

from nospy.keys import npubToHex, hexToNpub

from src.VERSION import VERSION

from src.common import (
    cprint,
    Colors,
    get,
    set,
    not_init,
    is_init,
)

from src.interface import column_fix

from src.settings import load_settings, save_settings




def run_home():
    cols2 = st.columns((1, 1, 1))

    with cols2[0]:
        if st.button("Run loop", disabled=st.session_state.run_loop):
            st.session_state.run_loop = not st.session_state.run_loop

    with cols2[1]:
        if st.session_state.run_loop:
            # if st.button("stop"):
            #     st.session_state.run_loop = False

            home()

            # st.write(time.time())
            # time.sleep(1)
            # st.rerun()


def run_inbox():
    cols2 = st.columns((1, 1, 1))

    with cols2[0]:
        if st.button("Run loop", disabled=st.session_state.run_loop):
            st.session_state.run_loop = not st.session_state.run_loop

    with cols2[1]:
        if st.session_state.run_loop:
            # if st.button("stop"):
            #     st.session_state.run_loop = False

            inbox()

            # st.write(time.time())
            # time.sleep(1)
            # st.rerun()



from nostr.key import PrivateKey

def private_to_public(private_key: str) -> str:
    """ provide a hex-encoded private key, and get back the hex-encoded public key """

    # Decode the hex-encoded private key
    priv = PrivateKey(bytes.fromhex(private_key))

    # Get the public key
    pub = priv.public_key.hex()

    return pub



def inbox():
    prv = st.session_state.settings["private_key"]
    prv = PrivateKey(bytes.fromhex(prv))
    pubkey = prv.public_key.hex()



    # filters = Filters([Filter(tags={'p': {pubkey}}, kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE])])
    filters = Filters([Filter(pubkey_refs=[pubkey], kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE])])

    subscription_id = uuid.uuid1().hex

    # create a relay manager and add our relays
    relay_manager = RelayManager()

    relays = st.session_state.settings["relays"]
    if relays == {}:
        st.error("You need to add a relay to run 'home'")
        st.stop()

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


    if st.button("stop"):
        st.session_state.run_loop = False

    while st.session_state.run_loop:
        # TODO: check if the websocket closes.. and reopen if needed.
        # TODO: I should probably break this up into a few functions...
        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()

            from_pub = event_msg.event.public_key
            # name = hex_following[from_pub]['name'] # look up the name we gave this person

            # st.write(event_msg.event.created_at)
            # st.write(event_msg.event.content)

            # msg = decrypt_direct_message(event_msg.event.content, prv)
            msg = prv.decrypt_message(event_msg.event.content, from_pub)

            st.write(msg)



            # update the last seen time for this author
            # TODO - still need this but has to be implemented differently
            # st.session_state.settings['following'][hexToNpub(from_pub)]['last_seen'] = event_msg.event.created_at
            # save_settings()



def home():
    # get the list of npubs we are following...
    following = st.session_state.settings["following"]

    print(following)

    following = [{"name": p[1]['name'], "p": p[0]} for p in following]

    st.write(following)


    # look for any entries that don't have a name, and give them a name (e.g. npub18~a2xw)
    # for f in following:
    #     npub = f['p']

    #     if f['name'] is None:
    #         f['name'] = f"{npub[:6]}~{npub[-4:]}"

    # convert the dict so that the public keys are hex-encoded - because that's what the relay manager expects
    hex_following = {npubToHex(f['p']) for f in following}

    st.write(hex_following)
    # st.stop()

    # This is our filter the tells the relay what we're looking for
    # filters = Filters(
    #     [
    #         Filter(
    #             authors=list(hex_following),
    #             kinds=[EventKind.TEXT_NOTE],
    #             since=int(time.time()) - 600, # 10 minutes ago
    #         )
    #     ]
    # )


    prv = st.session_state.settings["private_key"]

    my_pubkey = private_to_public(prv)





    inbox_mode = True
    if inbox_mode:
        # pubkey = getPubKey(Config.get_instance().private_key)
        filters = Filters([Filter(tags={'p': {my_pubkey}}, kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE])])
    else:
        filters = Filters([Filter(authors=list(hex_following.keys()), kinds=[EventKind.TEXT_NOTE])])

    subscription_id = uuid.uuid1().hex

    # create a relay manager and add our relays
    relay_manager = RelayManager()

    relays = st.session_state.settings["relays"]
    if relays == {}:
        st.error("You need to add a relay to run 'home'")
        st.stop()

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


    if st.button("stop"):
        st.session_state.run_loop = False

    while st.session_state.run_loop:
        # TODO: check if the websocket closes.. and reopen if needed.
        # TODO: I should probably break this up into a few functions...
        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()

            from_pub = event_msg.event.public_key
            # name = hex_following[from_pub]['name'] # look up the name we gave this person

            # st.write(event_msg.event.created_at)
            st.write(event_msg.event.content)



            # update the last seen time for this author
            st.session_state.settings['following'][hexToNpub(from_pub)]['last_seen'] = event_msg.event.created_at
            # for p in st.session_state.settings["following"]:
                # if p['p'] == from_pub:

            save_settings()

