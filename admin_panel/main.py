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

# from src.components.home import run_home, run_inbox



def init_if_needed():
    if is_init("setup"): # can't use init because ... apparently it's used for cookies..??
        return

    cprint(">>> Initializing Session State", Colors.CYAN)

    st.session_state.setup = True
    st.session_state.run_loop = False

    st.session_state.mode = "home"

    # if not_init("bots"):
    load_settings_files()

    # st.session_state.selected_bot = st.selectbox("Select Bot", st.session_state.bots)
    # if st.session_state.selected_bot is not None:
    #     load_settings()





def main_page():
    column_fix()
    cprint("\nmain()\n", Colors.YELLOW)

    # with centered_button_trick():
    with st.sidebar:
        st.header(":red[NOS]:green[4]:blue[A2] 🧛🏻‍♂️")
        st.caption(f"v{VERSION}")
        st.header("", divider="rainbow")


    # center_text("p", ":red[NOS]:green[4]:blue[A2]")

    # st.header(":red[NOS]:green[4]:blue[A2]")

    mobile = False


    with st.sidebar:
    # cside = st.columns((1, 1))
    # with cside[0]:
    # with centered_button_trick():
        st.session_state.selected_bot = st.selectbox("Select Bot", st.session_state.bots)
    
    # with cside[1]:

    if st.session_state.selected_bot is not None:
        load_settings()

    if mobile:
        cols = st.columns((1, 1))
        with cols[0]:
            keys_component()
    else:
        with st.sidebar:
            keys_component()

    # with cols[1]:
    # with st.sidebar:
    #     status_component()

    with st.sidebar:
        st.header("", divider="rainbow")

    with st.sidebar:
        st.button("💬 Replies", key="replies", use_container_width=True, on_click=lambda: setattr(st.session_state, 'mode', 'home'))
        st.button("📪 Inbox", key="inbox", use_container_width=True, on_click=lambda: setattr(st.session_state, 'mode', 'inbox'))
        st.button("🎯 status", key="status", use_container_width=True, on_click=lambda: setattr(st.session_state, 'mode', 'status'))

    with st.sidebar:
        st.header("", divider="rainbow")

    # cols2 = st.columns((1, 1))
    # with cols2[0]:
    with st.sidebar:
        follower_component()
    # with cols2[1]:
    with st.sidebar:
        relay_component()

    if st.session_state.mode == "home":
        post_component()
    elif st.session_state.mode == "inbox":
        database_view(st.session_state.selected_bot)
    elif st.session_state.mode == "status":
        status_component()

    # fetch_inbox()



    ### RUN LOOP (aka home)
    # st.header("", divider="rainbow")
    # run_home()
    # run_inbox()

    with st.sidebar:
        st.divider()

        new_bot_component()

        if os.getenv("DEBUG", False):
            st.warning("DEBUG MODE")
            with st.popover(":red[session state]"):
                st.write(st.session_state)
