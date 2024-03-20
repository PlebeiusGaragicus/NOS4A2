# import os
import pathlib
import json

import streamlit as st

from nosferatu.interface import column_fix, centered_button_trick, center_text
from nosferatu.settings import load_settings, load_settings_files

def new_bot_component():
    with st.popover("New Bot"):
        with st.form("new_bot_form"):
            st.text_input("Bot Name", key="new_bot_name")
            submit = st.form_submit_button("Create Bot")
            if submit:
                from nosferatu.settings import DEFAULT_SETTINGS

                bot_dir = pathlib.Path.home() / "bots" / st.session_state.new_bot_name
                # make new bot directory
                bot_dir.mkdir(exist_ok=True)
                with open(bot_dir / "settings.json", "w") as f:
                    json.dump( DEFAULT_SETTINGS, f, indent=4 )

                del st.session_state.setup # force init_if_needed to re-load all bot directories
                # TODO - I'm not a fan of the bot account always resetting to the first one in the list... perhaps we can make it a persistant UI element?
                st.rerun()
