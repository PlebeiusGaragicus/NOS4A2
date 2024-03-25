import streamlit as st

from pymongo import MongoClient

@st.cache_resource()
def database():
    client = MongoClient('localhost', 27017)
    db = client[ "nosferatu" ]

    return db
