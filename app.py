import streamlit as st
from menu import menu
from database.connect import engine
from database.tables import Model

st.session_state.initialized = False

if not st.session_state.initialized:

    Model.metadata.create_all(engine)
    st.session_state.initialized = True

menu()

st.title("Hello World! Home")
