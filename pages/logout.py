import streamlit as st
from menu import menu_with_redirect

menu_with_redirect()

st.title("로그아웃")
st.write(st.session_state.get("login"))

btn_logout = st.button('Logout')
if btn_logout:

    st.session_state.role = None
    choice = 'Home'
    st.rerun()
