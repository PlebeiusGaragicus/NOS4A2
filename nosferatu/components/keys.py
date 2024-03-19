import logging
logger = logging.getLogger("nosferatu")

import streamlit as st

from nosferatu.common import get
from nosferatu.keithmukai import Bip39PrivateKey
from nosferatu.settings import save_settings

from nostr.key import PrivateKey


def key_gen():
    # TODO - find a better way... we don't need this anymore because we aren't supplying a mnemonic
    pk = Bip39PrivateKey.with_mnemonic_length( 24 )
    st.session_state.settings["private_key"] = pk.hex()
    save_settings()
    st.rerun()


def keys_component():
    # st.header("", divider="rainbow")
    # st.markdown(f"### :red[Keys:]")

    with st.popover("🔑 :red[Keys:]"):
        if get('settings')['private_key'] in [None, ""]:
            st.write("No keys found.")
            if st.button("Generate Keys"):
                st.toast("Generating keys...", icon="🔑")
                key_gen()
        else:

            # prv = get('settings')['private_key']

            key = get('settings')['private_key']
            prv = PrivateKey( bytes.fromhex(key) )

            st.write(f"npub: `{prv.public_key.bech32()}`")
            st.write(f"npub hex: `{prv.public_key.hex()}`")

            st.write(f":red[nsec:] `{prv.bech32()}`")
            st.write(f":red[nsec hex:] `{prv.hex()}`")