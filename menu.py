import streamlit as st


st.set_page_config(layout="wide")


def authenticated_menu():
    st.sidebar.page_link("app.py", label="Home", icon=":material/home:")
    st.sidebar.page_link("pages/about.py", label="About", icon=":material/info:")
    st.sidebar.page_link("pages/theme.py", label="Theme", icon=":material/insert_chart:")
    st.sidebar.page_link("pages/setting.py", label="Setting", icon=":material/settings:")
    st.sidebar.page_link("pages/logout.py", label="LogOut", icon=":material/logout:")

    if st.session_state.role == "admin":
        st.sidebar.page_link("pages/admin.py", label="Admin", icon=":material/manage_search:")


def unauthenticated_menu():
    st.sidebar.page_link("app.py", label="Home", icon=":material/home:")
    st.sidebar.page_link("pages/about.py", label="About", icon=":material/info:")
    st.sidebar.page_link("pages/login.py", label="LogIn", icon=":material/login:")
    st.sidebar.page_link("pages/signin.py", label="SignIn", icon=":material/person_add:")


def menu():
    if st.session_state.get("role") is None:
        unauthenticated_menu()
    else:
        authenticated_menu()


def menu_with_redirect(allowed=("user", "admin")):
    if isinstance(allowed, str) or allowed is None:
        allowed = (allowed,)
    if st.session_state.get("role") not in allowed:
        st.switch_page("app.py")
    menu()
