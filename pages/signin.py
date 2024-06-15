import streamlit as st
from menu import menu_with_redirect
from database.tables import session, User

menu_with_redirect(allowed=None)

st.title("회원 가입")

with st.form("Signin Form"):

    first_name = st.text_input(label="First Name")
    last_name = st.text_input(label="Last Name")
    email = st.text_input(label="Email")
    password = st.text_input(label="Password")
    name = st.text_input(label="Name")

    button = st.form_submit_button(label="submit")

    if button:
        user = User(first_name=first_name, last_name=last_name, email=email, password=password, nickname=name)
        session.add(user)
        session.commit()

        st.session_state["role"] = "role"
        st.rerun()

st.write("회원 가입을 하는 것으로 사용자는 이용약관에 동의한 것으로 간주됩니다")