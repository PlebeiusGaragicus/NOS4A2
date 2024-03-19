import streamlit as st

from admin_panel.common import get
from admin_panel.components.keys import keys_component

def profile_component():
    st.header("🤖 :red[Profile]")
    st.header("", divider="rainbow")


    keys_component()

    st.write("picture")
