import os
import time
from datetime import datetime
import subprocess

from pymongo import MongoClient

import streamlit as st

from nostr.key import PrivateKey
from nosferatu.common import PROJECT_DIR, get
from nosferatu.keys import hexToNpub


def component():
    pass
    # cols2 = st.columns((1, 1, 1))
    # with cols2[1]:


def database_view():
    # st.divider()
    st.header("📪 :blue[Inbox]")
    st.header("", divider="rainbow")


    cols2 = st.columns((1, 1, 1))
    with cols2[0]:
        if st.button("run fetch"):
            # TODO - sanitize bot_name
            # TODO run f"nosferatu --fetch --name={st.session_state.botname}"
            # os.popen(f"nosferatu --fetch --name={st.session_state.selected_bot}")
            subprocess.run(["nosferatu_cli", "--bot_dir_name", st.session_state.selected_bot, "--fetch"])
            st.toast("Fetching...", icon="🔄")
            time.sleep(3)
            st.rerun()

    with cols2[1]:
        if st.button("Refresh"):
            st.rerun()

    bot_name = st.session_state.selected_bot
    # collection_name = bot_name

    from nosferatu.database import database
    db = database()
    # client = MongoClient('localhost', 27017)
    # db = client[ "nosferatu" ]
    key = get('settings')['private_key']
    if key in [None, ""]:
        st.error("Generate a key first!")
        return

    prv = PrivateKey( bytes.fromhex(key) )
    collection_name = str(prv.public_key.hex())
    collection = db[ collection_name ]

    # find all database entries with "kind": "ENCRYPTED_DIRECT_MESSAGE"
    cursor = collection.find({"kind": "ENCRYPTED_DIRECT_MESSAGE"}).sort("created_at", -1)
    st.toast("PULLING FROM DATABASE", icon="🥵")
    # TODO - I want to pull from the database on load, and when requested.
    # I don't want to pull from the database every time the page is refreshed (that is, for each on-page interaction)

    for document in cursor:
        from_pub = document["pubkey"]
        name = f":blue[anon]:red[-]:green[{from_pub[-8:]}]"
        for f in st.session_state.settings['following']:
            if f['npub'] == hexToNpub(from_pub):
                name = f['name']
                break

        with st.container(border=True):
            created_at = datetime.fromtimestamp(document["created_at"]).strftime('%B %d `%y - %H:%M:%S')
            st.write(f":green[{created_at}] | :blue[{name}]")
            # st.write(datetime.fromtimestamp(document["created_at"]).strftime('%B %d, %Y, %H:%M:%S'))
            st.write(document["clear_text"])

            cols3 = st.columns((1, 1, 1))
            with cols3[0]:
                delete = st.button("🗑️ :red[Delete]", key=document["_id"])
                if delete:
                    collection.delete_one({"_id": document["_id"]})
                    st.rerun()

            # with cols3[1]:
            with cols3[2].popover("..."):    
                block_purge = st.button("🔒 :red[Block & Purge]", key=f"blockpurge_{document['_id']}")
                if block_purge:
                    st.toast(f"Blocked and purged {name}", icon="🔒")
                    collection.delete_many({"pubkey": from_pub})
                    # TODO - add to block list
                    st.rerun()

            # TODO - follow this account and provide a name, if not followed

            # with cols3[2]:
            with cols3[2].popover("Event JSON"):
                st.write(document)
