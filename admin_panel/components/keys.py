import logging
logger = logging.getLogger("nospy")

import streamlit as st

from admin_panel.common import get
from admin_panel.keithmukai import Bip39PrivateKey
from admin_panel.settings import save_settings

from nostr.key import PrivateKey


def key_gen():
    # TODO - find a better way... we don't need this anymore because we aren't supplying a mnemonic
    pk = Bip39PrivateKey.with_mnemonic_length( 24 )
    st.session_state.settings["private_key"] = pk.hex()
    save_settings()
    st.rerun()


def keys_component():
    st.header("", divider="rainbow")
    st.markdown(f"### :red[Keys:]")

    if get('settings')['private_key'] in [None, ""]:
        st.write("No keys found.")
        if st.button("Generate Keys"):
            st.toast("Generating keys...", icon="🔑")
            key_gen()
    else:

        with st.popover("keys"):
            # prv = get('settings')['private_key']

            key = get('settings')['private_key']
            prv = PrivateKey( bytes.fromhex(key) )

            st.write(f"npub: `{prv.public_key.bech32()}`")
            st.write(f"npub hex: `{prv.public_key.hex()}`")

            st.write(f":red[nsec:] `{prv.bech32()}`")
            st.write(f":red[nsec hex:] `{prv.hex()}`")
