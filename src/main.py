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
from src.followers import add_new_follower, unfollow, follower_component
from src.relays import relay_component
from src.home import run_home, run_inbox



def init_if_needed():
    if is_init("setup"): # can't use init because ... apparently it's used for cookies..??
        return

    cprint(">>> Initializing Session State", Colors.CYAN)

    st.session_state.setup = True
    st.session_state.run_loop = False

    load_settings()














npub = "npub1gf0nzcjm6ug55wf9qxg4829237erxa00mzmcpzpd06a02xlk86xq33r3ht"

def main_page():
    column_fix()
    cprint("\nmain()\n", Colors.YELLOW)
    with st.popover(":red[session state]"):
        st.write(st.session_state)
    st.divider()


    ### BOT SETTINGS
    st.write(f"nsec: `{get('settings')['private_key']}`")
    st.write(npub)


    follower_component()
    relay_component()




    ### RUN LOOP (aka home)
    st.header("", divider="rainbow")
    # run_home()
    run_inbox()
