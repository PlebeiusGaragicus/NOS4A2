import time
import ssl
import logging
logger = logging.getLogger("nosferatu")

import streamlit as st

from nostr.event import Event
from nostr.relay_manager import RelayManager
from nostr.key import PrivateKey

from admin_panel.common import get


def connect_to_relays() -> RelayManager:
    relay_manager = RelayManager()
    relays = st.session_state.settings["relays"]
    for r in relays:
        relay_manager.add_relay(r['url'])

    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
    time.sleep(1.25) # allow the connections to open

    return relay_manager



def post_note(content: str):
    if not content or content == "":
        return

    relay_manager = connect_to_relays()

    priv = PrivateKey( bytes.fromhex(get('settings')['private_key']) )
    event = Event(
        content=content,
        public_key=priv.public_key.hex()
    )
    priv.sign_event(event)

    logger.debug("Publishing event...")
    relay_manager.publish_event(event)
    time.sleep(1) # allow the messages to send
    st.toast("Posted", icon="📬")

    relay_manager.close_connections()



def post_component():
    # st.header("", divider="rainbow")
    st.markdown(f"### :green[Post:]")

    content = st.text_area("Content", key="content")
    if st.button("Post"):
        post_note(content) # sleeps for 1 second
        st.rerun()
