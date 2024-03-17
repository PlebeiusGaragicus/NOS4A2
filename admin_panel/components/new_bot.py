import pathlib
import json

import streamlit as st

from admin_panel.interface import column_fix, centered_button_trick, center_text
from admin_panel.settings import load_settings, load_settings_files

def new_bot_component():
    with centered_button_trick():
        with st.popover("New Bot"):
            with st.form("new_bot_form"):
                st.text_input("Bot Name", key="new_bot_name")
                submit = st.form_submit_button("Create Bot")
                if submit:
                    return

                    bot_dir = pathlib.Path.home() / "bots"
                    with open(bot_dir / st.session_state.selected_bot / "settings.json", "w") as f:
                        pass
            # settings = json.load(f)
            # st.session_state.settings = json.load(f)