import os
import yaml
import time

import streamlit as st
import streamlit_authenticator as stauth

from src.common import ASSETS_PATH
from src.main import main_page, init_if_needed
from src.common import not_init, get, cprint, Colors

cprint(">>> Streamlit Server rerun~!", Colors.CYAN)


# @st.cache_resource(experimental_allow_widgets=True)
# def authenticator():
#     return stauth.Authenticate(
#         st.session_state.config["credentials"],
#         st.session_state.config["cookie"]["name"],
#         st.session_state.config["cookie"]["key"],
#         st.session_state.config["cookie"]["expiry_days"],
#         # config["preauthorized"],
#     )


def login_router_page():
    st.set_page_config(
        # page_title="" if os.getenv("DEBUG", False) else "NOS4A2",
        page_title="NOS4A2",
        page_icon=os.path.join(ASSETS_PATH, "favicon.ico"),
        layout="centered",
        initial_sidebar_state="auto",
    )

    if not_init("config"):
        try:
            with open("./auth.yaml") as file:
                st.session_state.config = yaml.safe_load(file)
        except FileNotFoundError:
            st.error("This instance has not been configured.  Missing `auth.yaml` file.")
            # TODO - just create an empty file and then re-run?  Put default root password in there and have user change it?
            st.stop()

    st.session_state.authenticator = stauth.Authenticate(
        st.session_state.config["credentials"],
        st.session_state.config["cookie"]["name"],
        st.session_state.config["cookie"]["key"],
        st.session_state.config["cookie"]["expiry_days"],
        # config["preauthorized"],
    )


    if st.session_state["authentication_status"] is None:
        if 'appstate' in st.session_state:
            # del st.session_state['appstate'] # <-----
            st.error("logout logic has not been created yet")
            st.error("Application state has been cleared!")

    if st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")

    # https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/
    # https://github.com/mkhorasani/Streamlit-Authenticator?ref=blog.streamlit.io
    st.session_state.authenticator.login(location="main", max_concurrent_users=1, fields={
        "Form name": "Bot c0mm4nd3r login",
        "Username": "Username",
        "Password": "Password",
        "Login": "Enter ye!",
    })

    if st.session_state["authentication_status"]:
        init_if_needed()
        main_page()
