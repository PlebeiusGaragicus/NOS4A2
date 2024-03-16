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

from src.keys import npubToHex, hexToNpub

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
        if f["npub"] == npub:
            st.toast("npub already exists", icon="❌")
            return

    st.session_state.settings["following"].append(
        {
            "name": name,
            "npub": npub,
            "last_seen": None,
        }
    )
    save_settings()




def unfollow(p):
    for f in st.session_state.settings["following"]:
        if f["npub"] == p:
            st.session_state.settings["following"].remove(f)

    save_settings()





def follower_component():
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
        # st.write(p)


        # st.divider()
        # st.text_input(label=f":green[{p['name']}]", value=p['p'])
        st.write(f":green[{p['name']}]", " : ", f":blue[{p['npub']}]")
        # st.write(p['p'])
        # st.button(":red[delete]", key=f"delete_{p}", on_click=unfollow, args=(p['p'],))

    