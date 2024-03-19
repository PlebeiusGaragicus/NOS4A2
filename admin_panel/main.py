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
from admin_panel.components.publish import post_component
from admin_panel.components.new_bot import new_bot_component
from admin_panel.components.inbox import database_view
from admin_panel.components.profile import profile_component

from admin_panel.keys import private_to_npub



def init_if_needed():
    if is_init("setup"): # can't use `init` because ... apparently it's used for cookies..??
        return

    cprint(">>> Initializing Session State", Colors.CYAN)

    st.session_state.setup = True
    # st.session_state.mode = "profile" # set starting page
    st.session_state.mode = PAGES[0]["mode"]


    load_settings_files()



PAGES = [
    {"label": "📪 :blue[Inbox]", "mode": "inbox", "callback": database_view},
    {"label": "✍️ :green[Post]", "mode": "post", "callback": post_component},
    {"label": "🤖 :red[Profile]", "mode": "profile", "callback": profile_component},
    {"label": "🐸 :orange[Frens]", "mode": "frens", "callback": follower_component},
    {"label": "📡 :grey[Relays]", "mode": "relays", "callback": relay_component},
    {"label": "🎯 :violet[Status]", "mode": "status", "callback": status_component},
]



def main_page():
    # column_fix() # this messes up the profile page...
    cprint("\nmain()\n", Colors.YELLOW)

    with st.sidebar:
        st.header(":red[NOS]:green[4]:blue[A2] 🧛‍♂️")
        st.caption(f"v{VERSION}")
        st.session_state.selected_bot = st.selectbox("Bot Account", st.session_state.bots)

    if st.session_state.selected_bot is not None:
        load_settings()

    with st.sidebar:
        name = st.session_state.settings.get("name", "Anonymous")
        # center_text("h1", f"{st.session_state.selected_bot}", )
        center_text("h1", f"{name}", )
        if npub := st.session_state.settings.get("private_key", None):
            short_pub = private_to_npub(npub)[-8:] + "..." + private_to_npub(npub)[-6:]
            # with st.popover(f":grey[npub]:green[{short_pub}]"):
            with st.popover(f"🔑 :rainbow[npub{short_pub}]", use_container_width=True):
                st.caption(private_to_npub(npub))
        else:
            st.warning("No private key set")

        # st.header("", divider="rainbow")
        # st.divider()
        center_text("p", "- - - - -")


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

