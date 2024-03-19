import streamlit as st

from admin_panel.settings import save_settings


def add_new_follower(name, npub):
    if not name or not npub:
        st.toast("Name and npub are required", icon="❓")
        return
    
    # check that npub is valid
    # if len(npub) != 66:
    #     st.toast("Invalid npub", icon="❌")
    #     return

    # check that name is unique
    for f in st.session_state.settings["following"]:
        if f["name"] == name:
            st.toast("Name already exists", icon="❌")
            return
    
    # check that npub is unique
    for f in st.session_state.settings["following"]:
        if f["npub"] == npub:
            st.toast("npub already exists", icon="❌")
            return

    st.session_state.settings["following"].append(
        {
            "name": name,
            "npub": npub,
            "last_seen": None,
        }
    )
    save_settings()




def unfollow(p):
    for f in st.session_state.settings["following"]:
        if f["npub"] == p:
            st.session_state.settings["following"].remove(f)

    save_settings()





def follower_component():
    ### FOLLOWING
    # st.header("", divider="rainbow")
    # st.markdown(f"### :blue[Following:]")

    with st.expander("🐸 :blue[Frens]"):

        mobile = False
        if mobile:
            cols2 = st.columns((1, 1, 1))
        else:
            cols2 = st.columns((1, 1))

        with cols2[0]:
            with st.popover("follow"):
                with st.form("new_follower"):
                    new_follower_name = st.text_input(label="name")
                    new_follower_npub = st.text_input(label="npub")
                    submit_button = st.form_submit_button(label="Add")

                    if submit_button:
                        add_new_follower(new_follower_name, new_follower_npub)

        with cols2[1]:
            with st.popover("Unfollow"):
                if unfollow_p := st.text_input(label="npub", key="unfollow"):
                    unfollow(unfollow_p)

        for p in st.session_state.settings["following"]:
            # st.text_input(label=f":green[{p['name']}]", value=p['p'])
            # short_pub = p["npub"][:10] + "..." + p["npub"][-10:]
            with st.container(border=True):
                # st.write(f":green[{p['name']}]", " : ", f":blue[{short_pub}]")
                st.write(f":green[{p['name']}]")
                st.write(f":blue[{p["npub"]}]")

                st.button(":red[delete]", key=f"delete_{p}", on_click=unfollow, args=(p['npub'],))
