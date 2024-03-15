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

