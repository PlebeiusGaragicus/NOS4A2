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

from nospy.keys import npubToHex

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



def load_settings():
    try:
        with open("settings.json", "r") as f:
            # settings = json.load(f)
            st.session_state.settings = json.load(f)

    except FileNotFoundError:
        st.error("settings.json not found")
        st.stop()
    except json.JSONDecodeError:
        st.error("settings.json is not valid JSON")
        st.stop()


def save_settings():
    with open("settings.json", "w") as f:
        json.dump(st.session_state.settings, f, indent=4)


def init_if_needed():
    if is_init("setup"): # can't use init because ... apparently it's used for cookies..??
        return

    cprint(">>> Initializing Session State", Colors.CYAN)

    st.session_state.setup = True
    st.session_state.run_loop = False

    load_settings()



def add_new_follower(name, npub):
    if not name or not npub:
        st.toast("Name and npub are required", icon="❓")
        return
    
    # check that npub is valid
    # if len(npub) != 66:
    #     st.toast("Invalid npub", icon="❌")
    #     return

    # check that name is unique
    for f in st.session_state.settings["following"]:
        if f["name"] == name:
            st.toast("Name already exists", icon="❌")
            return
    
    # check that npub is unique
    for f in st.session_state.settings["following"]:
        if f["p"] == npub:
            st.toast("npub already exists", icon="❌")
            return

    st.session_state.settings["following"].append({"name": name, "p": npub})
    save_settings()


def unfollow(p):
    for f in st.session_state.settings["following"]:
        if f["p"] == p:
            st.session_state.settings["following"].remove(f)

    save_settings()



def main_page():
    column_fix()
    cprint("\nmain()\n", Colors.YELLOW)
    with st.popover(":red[session state]"):
        st.write(st.session_state)
    st.divider()



    ### BOT SETTINGS
    st.write(f"nsec: `{get('settings')['private_key']}`")



    ### FOLLOWING
    st.header("", divider="rainbow")
    st.markdown(f"## :orange[Following:]")

    cols2 = st.columns((1, 1, 1))

    with cols2[0]:
        with st.popover("follow"):
            with st.form("new_follower"):
                new_follower_name = st.text_input(label="name")
                new_follower_npub = st.text_input(label="npub")
                submit_button = st.form_submit_button(label="Add")

                if submit_button:
                    add_new_follower(new_follower_name, new_follower_npub)

    with cols2[1]:
        with st.popover("Unfollow"):
            if unfollow_p := st.text_input(label="npub", key="unfollow"):
                unfollow(unfollow_p)

    for p in st.session_state.settings["following"]:


        # st.divider()
        # st.text_input(label=f":green[{p['name']}]", value=p['p'])
        st.write(f":green[{p['name']}]", " : ", f":blue[{p['p']}]")
        # st.write(p['p'])
        # st.button(":red[delete]", key=f"delete_{p}", on_click=unfollow, args=(p['p'],))

    
        




    ### RELAYS
    st.header("", divider="rainbow")
    st.markdown(f"## :orange[Relays:]")

    for r in st.session_state.settings["relays"]:
        # st.text_input(label="relay", value=r)
        st.write(f":green[{r['url']}]")

    st.header("", divider="rainbow")
    run_loop()






def run_loop():
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









def home():
    # get the list of npubs we are following...
    following = st.session_state.settings["following"]

    # look for any entries that don't have a name, and give them a name (e.g. npub18~a2xw)
    # for f in following:
    #     npub = f['p']

    #     if f['name'] is None:
    #         f['name'] = f"{npub[:6]}~{npub[-4:]}"

    # convert the dict so that the public keys are hex-encoded - because that's what the relay manager expects
    hex_following = {npubToHex(f['p']) for f in following}

    # This is our filter the tells the relay what we're looking for
    filters = Filters([Filter(authors=list(hex_following), kinds=[EventKind.TEXT_NOTE])]) # TEXT_NOTE
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

            st.write(event_msg.event.content)
