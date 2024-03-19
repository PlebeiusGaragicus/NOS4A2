import os

import streamlit as st

from admin_panel.VERSION import VERSION
from admin_panel.common import (
    cprint,
    Colors,
    get,
    set,
    not_init,
    is_init,
)

from admin_panel.interface import column_fix, centered_button_trick, center_text
from admin_panel.settings import load_settings, load_settings_files

from admin_panel.components.followers import follower_component
from admin_panel.components.relays import relay_component
from admin_panel.components.status import status_component
from admin_panel.components.keys import keys_component
from admin_panel.components.publish import post_component
from admin_panel.components.new_bot import new_bot_component
from admin_panel.components.fetch_inbox import fetch_inbox
from admin_panel.components.database_view import database_view
from admin_panel.components.profile import profile_component

# from admin_panel.components.home import private_to_public
from admin_panel.keys import private_to_npub

# from src.components.home import run_home, run_inbox



def init_if_needed():
    if is_init("setup"): # can't use init because ... apparently it's used for cookies..??
        return

    cprint(">>> Initializing Session State", Colors.CYAN)

    st.session_state.setup = True
    st.session_state.run_loop = False

    st.session_state.mode = "profile"

    # if not_init("bots"):
    load_settings_files()

    # st.session_state.selected_bot = st.selectbox("Select Bot", st.session_state.bots)
    # if st.session_state.selected_bot is not None:
    #     load_settings()



PAGES = [
    {"label": "✍️ :green[Post]", "mode": "post", "callback": post_component},
    {"label": "📪 :blue[Inbox]", "mode": "inbox", "callback": database_view},
    {"label": "🐸 :orange[Frens]", "mode": "frens", "callback": follower_component},
    {"label": "🤖 :red[Profile]", "mode": "profile", "callback": profile_component},
    {"label": "📡 :grey[Relays]", "mode": "relays", "callback": relay_component},
    {"label": "🎯 :violet[Status]", "mode": "status", "callback": status_component},
]



def main_page():
    # column_fix()
    cprint("\nmain()\n", Colors.YELLOW)

    with st.sidebar:
        # st.header(":red[NOS]:green[4]:blue[A2] 🧛🏻‍♂️")
        st.header(":red[NOS]:green[4]:blue[A2] 🧛‍♂️")
        # st.header("", divider="rainbow")
        st.session_state.selected_bot = st.selectbox("Bot Account", st.session_state.bots)

        st.caption(f"v{VERSION}")

    # with st.sidebar:

    if st.session_state.selected_bot is not None:
        load_settings()

    with st.sidebar:
        npub = st.session_state.settings.get("private_key", "No private key set")
        st.caption(private_to_npub(npub))

    with st.sidebar:
        st.header("", divider="rainbow")

    for b in PAGES:
        if st.sidebar.button(b["label"], use_container_width=True):
            setattr(st.session_state, 'mode', b["mode"])

    for b in PAGES:
        if st.session_state.mode == b["mode"]:
            b["callback"]()


    with st.sidebar:
        new_bot_component()

        if os.getenv("DEBUG", False):
            st.header("", divider="rainbow")
            st.error("DEBUG MODE")
            with st.popover(":red[session state]"):
                st.write(st.session_state)

