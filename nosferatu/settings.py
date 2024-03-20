import os
import json
import pathlib

import streamlit as st


DEFAULT_RELAYS = [
    {
        "url": "wss://relay.damus.io",
        "read": True,
        "write": True
    },
    {
        "url": "wss://relay.snort.social",
        "read": True,
        "write": True
    },
    {
        "url": "wss://relay.primal.net",
        "read": True,
        "write": True
    }
]

DEFAULT_SETTINGS = {
    "private_key": None,
    "following": [],
    "relays": DEFAULT_RELAYS,
}

def load_settings_files():
    try:
        bot_dir = pathlib.Path.home() / "bots"
        files = os.listdir(bot_dir)
        # remove "DISABLED BOTS" from the list
        bots = [f for f in files if os.path.isdir(bot_dir / f)]

        for f in bots:
            if f == "DISABLED_BOTS":
                bots.remove(f)
                break

        if len(bots) == 0:
            st.error("No bots found in ~/bots")
            # make an empty directory inside ~/bots
            os.makedirs(bot_dir / "DISABLED_BOTS", exist_ok=True)
            os.makedirs(bot_dir / "my_first_bot", exist_ok=True)
            # st.stop()
            st.rerun()

        # st.session_state.bots = [f for f in files if os.path.isdir(bot_dir / f)]
        st.session_state.bots = bots
    except FileNotFoundError:
        st.error("bots directory not found")
        st.stop()



def load_settings():
    try:
        # with open("settings.json", "r") as f:

        bot_dir = pathlib.Path.home() / "bots"
        with open(bot_dir / st.session_state.selected_bot / "settings.json", "r") as f:
            # settings = json.load(f)
            st.session_state.settings = json.load(f)

    except FileNotFoundError:
        # st.error("settings.json not found")
        # st.stop()
        st.session_state.settings = DEFAULT_SETTINGS
        with open(bot_dir / st.session_state.selected_bot / "settings.json", "w") as f:
            json.dump(st.session_state.settings, f, indent=4)

        st.toast("settings.json not found, created new settings.json", icon="🟢")

    except json.JSONDecodeError:
        st.error("settings.json is not valid JSON")
        st.stop()


def save_settings():
    # with open("settings.json", "w") as f:
    bot_dir = pathlib.Path.home() / "bots"

    with open(bot_dir / st.session_state.selected_bot / "settings.json", "w") as f:
        json.dump(st.session_state.settings, f, indent=4)

