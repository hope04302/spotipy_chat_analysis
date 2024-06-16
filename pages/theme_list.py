import streamlit as st
from time import time
from menu import menu, set_query
from database.tables import Analysis

menu()
set_query()

analysis_id = st.session_state.query.get("id")
if analysis_id is None:
    st.switch_page('app.py')

a = Analysis.filter_id(analysis_id)
if a is None:
    st.switch_page('app.py')

st.title("temp")
p = a.result_cluster

for i in range(len(p)):
    st.title(i)
    st.write(p[str(i)])
