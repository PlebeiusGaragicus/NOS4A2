import os
import time
import datetime
import json
import uuid
import ssl
from websocket._exceptions import WebSocketConnectionClosedException

import streamlit as st

from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import PublicKey, PrivateKey

from nosferatu.keys import npubToHex, hexToNpub

from nosferatu.VERSION import VERSION



def fetch_inbox():
    st.divider()
    st.header("Inbox 📪")

    cols2 = st.columns((1, 1, 1))
    with cols2[1]:
        fetched_time = st.empty()

    # read the last updated time from the "last_updated.json" file inside bot/dm folder
    bot_dir = os.path.join(os.path.expanduser("~"), "bots")
    dm_dir = os.path.join(bot_dir, st.session_state.selected_bot, "dm")
    last_updated_file = os.path.join(dm_dir, "last_updated.json")
    try:
        with open(last_updated_file, "r") as f:
            last_updated = json.load(f)["last_updated"]

        # st.write("last updated:", datetime.datetime.fromtimestamp(last_updated).strftime('%Y-%m-%d %H:%M:%S'))
        # st.write("current time:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        min_since_last_update = (datetime.datetime.now().timestamp() - last_updated) / 60
        if min_since_last_update < 1:
            with cols2[1]:
                fetched_time.write(f"Updated now")
        elif min_since_last_update < 60:
            with cols2[1]:
                fetched_time.write(f"Updated {min_since_last_update:.1f} minutes ago")
        else:
            with cols2[1]:
                fetched_time.write(f"Updated {min_since_last_update/60:.1f} hours ago")

        # with cols2[1]:
        #     st.write(f"Update: {:.1f}")
    except (FileNotFoundError, json.JSONDecodeError):
        last_updated = None
        with cols2[1]:
            fetched_time.write(f"Never fetched")

    with cols2[0]:
        fetch = st.button("Fetch Inbox")

    if fetch:
        with st.spinner("Fetching Inbox"):
            fetched_time.empty()
            fetched_time.write("Updated now.")
            inbox(last_updated)


def private_to_public(private_key: str) -> str:
    """ provide a hex-encoded private key, and get back the hex-encoded public key """

    # Decode the hex-encoded private key
    priv = PrivateKey(bytes.fromhex(private_key))

    # Get the public key
    pub = priv.public_key.hex()

    return pub



def inbox(last_updated):
    prv = st.session_state.settings["private_key"]
    prv = PrivateKey(bytes.fromhex(prv))
    pubkey = prv.public_key.hex()

    

    if last_updated is not None:
        filters = Filters([Filter(pubkey_refs=[pubkey], kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE], since=last_updated)])
    else:
        filters = Filters([Filter(pubkey_refs=[pubkey], kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE])])

    subscription_id = uuid.uuid1().hex
    relay_manager = RelayManager()

    relays = st.session_state.settings["relays"]
    if relays == {}:
        st.error("You need to add a relay to run 'home'")
        st.stop()

    for r in relays:
        if r['read'] == True:
            relay_manager.add_relay(r['url'], r['read'], r['write'])

    relay_manager.add_subscription(subscription_id, filters)
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification

    # create a request message to send to the relay
    request = [ClientMessageType.REQUEST, subscription_id]
    request.extend(filters.to_json_array())
    message = json.dumps(request)

    # send the request to the relay
    time.sleep(1.25) # allow the connections to open
    try:
        relay_manager.publish_message(message) # send the request to the relay
    except WebSocketConnectionClosedException as e:
        # st.exception(e)
        st.error("Error connecting to a relay")
        st.stop()
    time.sleep(1) # allow the messages to send



    # TODO: check if the websocket closes.. and reopen if needed.
    # TODO: I should probably break this up into a few functions...
    no_new_messages = True
    while relay_manager.message_pool.has_events():
        event_msg = relay_manager.message_pool.get_event()

        from_pub = event_msg.event.public_key
        msg = prv.decrypt_message(event_msg.event.content, from_pub)

        sender_npub = hexToNpub(from_pub)

        with st.container(border=True):
            # short_npub = sender_npub[:8] + "..." + sender_npub[-8:]


            # search followers for the name, if we are following them
            # NOTE: alternatively, we could pull profile info from a relay (expensive)
            name = f":blue[anon]:red[-]:green[{sender_npub[-8:]}]"
            for f in st.session_state.settings['following']:
                if f['npub'] == hexToNpub(from_pub):
                    name = f['name']
                    break



            st.write(f"From: :blue[{name}]")
            st.write(msg)

            with st.popover("event"):
                st.write(event_msg.subscription_id)
                st.write(f"relay: {event_msg.url}")
                st.write(event_msg.event.created_at)
                st.write(f"tags: {event_msg.event.tags}")
                st.write(f"id: {event_msg.event.id}")
                # self.public_key = public_key
                # self.content = content
                # self.created_at = created_at or int(time.time())
                # self.kind = kind
                # self.tags = tags
                # self.signature = signature
                # self.id = i

        no_new_messages = False


    if no_new_messages:
        st.warning("No new messages")


        # update the last seen time for this author
        # TODO - still need this but has to be implemented differently
        # st.session_state.settings['following'][hexToNpub(from_pub)]['last_seen'] = event_msg.event.created_at
        # save_settings()

    # write "last_updated.json" file inside bot/dm folder
    bot_dir = os.path.join(os.path.expanduser("~"), "bots")
    dm_dir = os.path.join(bot_dir, st.session_state.selected_bot, "dm")
    last_updated_file = os.path.join(dm_dir, "last_updated.json")
    # ensure folder exists
    os.makedirs(dm_dir, exist_ok=True)
    with open(last_updated_file, "w") as f:
        json.dump({"last_updated": int(time.time())}, f, indent=4)
