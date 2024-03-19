import streamlit as st

from admin_panel.common import get

def status_component():
    st.write("✅ :green[Running]")

    return
    # st.header("", divider="rainbow")
    # st.markdown(f"### :blue[Status:]")

    # with st.container(border=True):
    with st.popover("🎯 :green[status]"):
        st.caption("none")
