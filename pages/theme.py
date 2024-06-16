import streamlit as st
from menu import menu
from database.tables import Analysis

menu()

st.title("주제별 노래 정리")

col1, col2 = st.columns(2)

analyses = Analysis.query.all()
analyses += ["plus_area"]


def one_component(_cont, analysis):

    if analysis != "plus_area":

        _cont.title(analysis.name)
        _cont.write(analysis.created_at)
        _cont.write(analysis.updated_at)

        btn = _cont.button("입장", key=analysis.name)

        if btn:
            st.session_state.query = {"id": analysis.id}
            st.switch_page("pages/theme_list.py")

    else:

        _cont.title("Try to plus your analysis!")

        btn = _cont.button("+++++", key="_plus_area")      # 겹칠 수도...?

        if btn:
            st.switch_page("pages/theme_add.py")


for i, analysis in enumerate(analyses):
    if i % 2 == 0:
        tile1 = col1.container(border=True)
        one_component(tile1, analysis)
    else:
        tile2 = col2.container(border=True)
        one_component(tile2, analysis)
