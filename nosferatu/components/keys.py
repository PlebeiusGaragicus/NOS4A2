import logging
logger = logging.getLogger("nosferatu")

import streamlit as st

from nostr.key import PrivateKey

from nosferatu.common import get
from nosferatu.keys import nsecToHex
from nosferatu.keithmukai import Bip39PrivateKey
from nosferatu.settings import save_settings



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
            
            with st.form("Import key"):
                st.text_input("nsec", key="nsec")
                if st.form_submit_button("Import"):
                    nsec_hex = nsecToHex( st.session_state.nsec )
                    prv_hex = PrivateKey( bytes.fromhex( nsec_hex ) ).hex()
                    st.session_state.settings["private_key"] = prv_hex
                    save_settings()
                    st.rerun()
        else:

            # prv = get('settings')['private_key']

            key = get('settings')['private_key']
            prv = PrivateKey( bytes.fromhex(key) )

            st.write(f"npub: `{prv.public_key.bech32()}`")
            st.write(f"npub hex: `{prv.public_key.hex()}`")

            st.write(f":red[nsec:] `{prv.bech32()}`")
            st.write(f":red[nsec hex:] `{prv.hex()}`")
