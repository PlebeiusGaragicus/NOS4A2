import streamlit as st

from admin_panel.common import get

def status_component():
    st.header("", divider="rainbow")
    st.markdown(f"### :blue[Status:]")

    with st.container(border=True):
        st.write("✅ :green[Running]")