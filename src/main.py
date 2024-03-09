import os
import json

import streamlit as st

from src.VERSION import VERSION

from src.common import (
    cprint,
    Colors
)




def init_if_needed():
    pass


def main_page():
    cprint("\n\nmain()\n", Colors.YELLOW)
    st.write("Hello, world!")