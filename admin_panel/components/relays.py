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

from admin_panel.keys import npubToHex, hexToNpub

from admin_panel.VERSION import VERSION

from admin_panel.common import (
    cprint,
    Colors,
    get,
    set,
    not_init,
    is_init,
)

from admin_panel.interface import column_fix

from admin_panel.settings import load_settings, save_settings



def add_relay(url, read, write):
    if not url:
        st.toast("URL is required", icon="❓")
        return

    for r in st.session_state.settings["relays"]:
        if r["url"] == url:
            st.toast("URL already exists", icon="❌")
            return

    st.session_state.settings["relays"].append(
        {
            "url": url,
            "read": read,
            "write": write,
        }
    )

    save_settings()
    st.toast("Relay added", icon="🟢")
    # st.rerun()


def remove_relay(url):
    st.session_state.settings["relays"] = [r for r in st.session_state.settings["relays"] if r["url"] != url]
    save_settings()
    st.toast("Relay removed", icon="🔴")
    # st.rerun()




def relay_component():
    st.header("", divider="rainbow")
    st.markdown(f"### :green[Relays:]")

    cols2 = st.columns((1, 1, 1))

    with cols2[0]:
        with st.popover("add"):
            with st.form("new_relay"):
                relay_url = st.text_input(label="relay url")
                read = st.checkbox(label="read from", value=True)
                write = st.checkbox(label="write to", value=True)
                if st.form_submit_button("Add Relay"):
                    add_relay(relay_url, read, write)

    with cols2[1]:
        with st.popover("remove"):
            with st.form("remove_relay"):
                remove_relay_url = st.text_input(label="relay url")
                if st.form_submit_button("Remove Relay"):
                    remove_relay(remove_relay_url)

    for r in st.session_state.settings["relays"]:
        # st.text_input(label="relay", value=r)
        read = "✅" if r["read"] else "❌"
        write = "✅" if r["write"] else "❌"
        with st.container(border=True):
            st.write(f":green[{r['url']}]")
            st.write(f"Read: {read} --- Write: {write}")
