import streamlit as st
from menu import menu_with_redirect
from database.tables import User

menu_with_redirect(allowed=None)

st.title("로그인")
st.write(st.session_state.get("login"))

with st.form("Login Form"):
    email = st.text_input(label="Email")
    password = st.text_input(label="Password")

    button = st.form_submit_button(label="submit")

    if button:
        idToken = User.verify_login(email, password)
        if idToken is None:
            st.error("아이디, 비밀번호를 다시 확인하세요.")
        else:
            st.session_state.role = "user"
            choice = 'Theme'
            st.rerun()

# st.write("비밀번호가 기억나지 않나요?")
#
# n_btn = st.button("비밀번호 재설정")
# if n_btn:
#     st.switch_page("pages/password_reset.py")