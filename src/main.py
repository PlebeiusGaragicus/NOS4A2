import streamlit as st

from src.VERSION import VERSION
from src.common import (
    cprint,
    Colors,
    get,
    set,
    not_init,
    is_init,
)

from src.interface import column_fix, centered_button_trick, center_text
from src.settings import load_settings, load_settings_files

from src.components.followers import follower_component
from src.components.relays import relay_component
from src.components.status import status_component
from src.components.keys import keys_component
from src.components.publish import post_component
from src.components.new_bot import new_bot_component
from src.components.fetch_inbox import fetch_inbox

# from src.components.home import run_home, run_inbox



def init_if_needed():
    if is_init("setup"): # can't use init because ... apparently it's used for cookies..??
        return

    cprint(">>> Initializing Session State", Colors.CYAN)

    st.session_state.setup = True
    st.session_state.run_loop = False

    # if not_init("bots"):
    load_settings_files()

    # st.session_state.selected_bot = st.selectbox("Select Bot", st.session_state.bots)
    # if st.session_state.selected_bot is not None:
    #     load_settings()





def main_page():
    column_fix()
    cprint("\nmain()\n", Colors.YELLOW)

    with centered_button_trick():
        st.header(":red[NOS]:green[4]:blue[A2] 🧛🏻‍♂️")
        st.caption(f"v{VERSION}")

    # center_text("p", ":red[NOS]:green[4]:blue[A2]")

    # st.header(":red[NOS]:green[4]:blue[A2]")




    cside = st.columns((1, 1))
    with cside[0]:
    # with centered_button_trick():
        st.session_state.selected_bot = st.selectbox("Select Bot", st.session_state.bots)
    
    with cside[1]:
        new_bot_component()
                    

    if st.session_state.selected_bot is not None:
        load_settings()

    cols = st.columns((1, 1))

    with cols[0]:
        keys_component()

    with cols[1]:
        status_component()

    cols2 = st.columns((1, 1))
    with cols2[0]:
        follower_component()
    with cols2[1]:
        relay_component()

    post_component()

    fetch_inbox()



    ### RUN LOOP (aka home)
    # st.header("", divider="rainbow")
    # run_home()
    # run_inbox()
    st.divider()
    with st.popover(":red[session state]"):
        st.write(st.session_state)
