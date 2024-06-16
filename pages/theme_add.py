import streamlit as st
from menu import menu, set_query
from database.tables import Analysis
import requests

menu()

st.title("주제별 노래 정리")

if 'advance_set' not in st.session_state:
    st.session_state.advance_set = False

# 버튼 클릭 시 상태 변경 함수
def change():
    st.session_state.advance_set = not st.session_state.advance_set

# 버튼 상태에 따라 다른 라벨 표시
if st.session_state.advance_set:
    setting = st.button("심화 설정", on_click=change)
else:
    setting = st.button("기본 설정", on_click=change)

with st.form("Theme add form"):

    name = st.text_input(label="project_name")

    playlists = st.text_input(label="playlists of spotipy")

    english_nltk = st.radio(label="english_tokenizer", options=["nltk"], index=0)
    korean_nltk = st.radio(label="korean_tokenizer", options=["okt", "kkma", "komoran"], index=0)

    stopwords = st.text_area(label="stopword adding")

    vectorize = st.radio(label="vector", options=["WoB(PTM)", "tf-idf"], index=0)

    topic_find_model = st.radio(label="topic model", options=["lsa", "plsa", "lda"], index=2)
    fav_coef = st.radio(label="fav coef", options=["perplexity", "coherence"], index=0)

    clustering = st.radio(label="fav clustering", options=["K-means", "DBSCAN"], index=0)

    bth = st.form_submit_button(label="summit!")

    if bth:
        data = {
            "playlists_id": playlists.split(),
            "english_nltk": english_nltk,
            "korean_nltk": korean_nltk,
            "stopwords": stopwords.split('\n'),
            "vectorize": vectorize,
            "topic_find_model": topic_find_model,
            "fav_coef": fav_coef,
            "clustering": clustering,
        }
        response = requests.post('http://127.0.0.1:8000/predict', json=data)



















