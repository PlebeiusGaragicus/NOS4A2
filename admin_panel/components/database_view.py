from pymongo import MongoClient
from datetime import datetime

import streamlit as st

from admin_panel.keys import hexToNpub


def component():
    pass
    # cols2 = st.columns((1, 1, 1))
    # with cols2[1]:


def database_view(bot_name):
    # st.divider()
    st.header("Inbox 📪")

    client = MongoClient('localhost', 27017)

    db = client[ "nosferatu" ]
    collection_name = bot_name
    collection = db[ collection_name ]

    # find all database entries with "kind": "ENCRYPTED_DIRECT_MESSAGE"
    cursor = collection.find({"kind": "ENCRYPTED_DIRECT_MESSAGE"}).sort("created_at", -1)

    for document in cursor:
        from_pub = document["pubkey"]
        name = f":blue[anon]:red[-]:green[{from_pub[-8:]}]"
        for f in st.session_state.settings['following']:
            if f['npub'] == hexToNpub(from_pub):
                name = f['name']
                break

        with st.container(border=True):
            st.write(f"From: :blue[{name}]")
            st.write(datetime.fromtimestamp(document["created_at"]).strftime('%B %d, %Y, %H:%M:%S'))
            st.write(document["clear_text"])

            with st.popover("..."):
                delete = st.button("🗑️ :red[Delete]", key=document["_id"])
                if delete:
                    collection.delete_one({"_id": document["_id"]})
                    st.rerun()
                
                block_purge = st.button("🔒 :red[Block & Purge]", key=f"blockpurge_{document["_id"]}")
                if block_purge:
                    st.toast(f"Blocked and purged {name}", icon="🔒")
                    collection.delete_many({"pubkey": from_pub})
                    # TODO - add to block list
                    st.rerun()
