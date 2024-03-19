import os

import streamlit as st

from admin_panel.common import get
from admin_panel.components.keys import keys_component

from admin_panel.settings import save_settings

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEFAULT_PROFILE_PIC = str(PROJECT_DIR + "/profile.png")
DEFAULT_BANNER_PIC = str(PROJECT_DIR + "/banner.png")

def profile_component():
    st.header("🤖 :red[Profile]")
    st.header("", divider="rainbow")


    keys_component()

    pic_url = get("settings").get("profile_url", None)
    with st.container(border=True):
        cols2 = st.columns((1, 3))
        with cols2[0]:
            if pic_url:
                try:
                    st.image(pic_url)
                except st.runtime.media_file_storage.MediaFileStorageError:
                    st.error("Error loading profile pic")
                    # st.image(DEFAULT_PROFILE_PIC, caption="No profile pic set", use_column_width=True)
            else:
                st.image(DEFAULT_PROFILE_PIC, caption="No profile pic set", use_column_width=True)
            st.markdown(f"### {get('settings').get('name', '')}")
            # st.write(get("settings").get("name", None))

            # st.write(f"`lud16:`\n{get('settings').get('lud16', '')}")
            # st.write(f"`nip05:`\n{get('settings').get('nip05', '')}")
            # st.write(f"`website:`\n{get('settings').get('website', '')}")

        ban_url = get("settings").get("banner_url", None)
        with cols2[1]:
            # with st.container(border=True):
            if ban_url:
                try:
                    st.image(ban_url)
                except st.runtime.media_file_storage.MediaFileStorageError:
                    st.error("Error loading banner pic")
                    # st.image(DEFAULT_BANNER_PIC, caption="No profile pic set", use_column_width=True)
            else:
                st.image(DEFAULT_BANNER_PIC, caption="No banner pic set", use_column_width=True)


        st.write(f"`Bio:` {get('settings').get('bio', '')}")
        # st.write(f"`lud16:` {get('settings').get('lud16', '')}")
        if get('settings').get('lud16', None) not in [None, ""]:
            st.link_button(f"`lud16:` {get('settings').get('lud16', '')}", url=f"lightning:{get('settings').get('lud16', '')}")
        else:
            st.write(f"`lud16:` --")
        st.write(f"`nip05:` {get('settings').get('nip05', '')}")
        st.write(f"`website:` {get('settings').get('website', '')}")

    with st.form(key="profile_form"):
        st.markdown("## :orange[Edit Profile]")
        name = st.text_input("Display Name", value=get("settings").get("name", None))
        profile_url = st.text_input("Profile pic URL", value=pic_url)
        banner_url = st.text_input("Banner URL", value=ban_url)
        bio = st.text_area("About me", value=get("settings").get("bio", None))
        lud16 = st.text_input("lightning address (lud16)", value=get("settings").get("lud16", None))
        nip05 = st.text_input("Nostr address (nip-05)", value=get("settings").get("nip05", None))
        website = st.text_input("website", value=get("settings").get("website", None))

        # submit = st.form_submit_button("save profile")
        # if submit:
        if st.form_submit_button(":green[Save Profile]"):
            st.session_state.settings["name"] = name
            st.session_state.settings["profile_url"] = profile_url
            st.session_state.settings["banner_url"] = banner_url
            st.session_state.settings["bio"] = bio
            st.session_state.settings["lud16"] = lud16
            st.session_state.settings["nip05"] = nip05
            st.session_state.settings["website"] = website

            save_settings()
            st.rerun()


    if st.button(":orange[Broadcast to relays] 📡"):
        st.toast("Not yet implemented", icon="🚧")
    
    with st.popover(":grey[settings json file]"):
        st.write(st.session_state.settings)
