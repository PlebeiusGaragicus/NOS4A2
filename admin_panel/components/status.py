import streamlit as st

from admin_panel.common import get

def status_component():
    st.header(":violet[🎯 Status]")
    # st.markdown(f"### :blue[Status:]")
    st.header("", divider="rainbow")

    st.write("✅ :green[Running]")
    st.write("🔗 :blue[Connected to the network]")
