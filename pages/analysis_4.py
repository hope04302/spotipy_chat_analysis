import streamlit as st
from common_container import menu
from data_analysis import lda_result_df, song_df

import pyLDAvis
import pyLDAvis.gensim_models
import streamlit.components.v1
from gensim.corpora import Dictionary

st.set_page_config(layout="wide")
menu()

st.sidebar.divider()
with st.form(key="by"):
    with st.sidebar:
        N = st.number_input("n_topic", min_value=2, max_value=50)
        st.form_submit_button("apply")


@st.experimental_fragment
def frag1():
    st.title("LDA 분석을 통한 토픽 개수 정하기")
    st.divider()
    st.write("LDA 모델에서 n을 달리하며 학습했을 때 perplexity와 coherence의 변화")
    st.divider()

    col1, col2 = st.columns(2)
    col1.line_chart(data=lda_result_df, y="perplexity")
    col2.line_chart(data=lda_result_df, y="coherence")


# @st.experimental_fragment
def frag2():
    st.title("LDA 분석을 통한 토픽의 핵심 단어 지정하기")
    st.divider()
    st.write("사이드바의 n을 변화시켜가며 토픽이 어떻게 나오는지 확인해보자.")
    id2word = Dictionary(song_df["tk_lyrics"])

    id2word.filter_extremes(no_below=5)

    corpus = [id2word.doc2bow(text) for text in song_df["tk_lyrics"]]

    lda_display = pyLDAvis.gensim_models.prepare(lda_result_df.loc[N, "lda_model"], corpus, id2word)

    # HTML 파일로 저장
    pyLDAvis.save_html(lda_display, 'lda.html')

    # HTML 파일 읽기
    with open('lda.html', 'r', encoding='utf-8') as f:
        html_string = f.read()

    # HTML을 iframe으로 표시
    st.components.v1.html(html_string, width=1300, height=800)


frag1()
st.write(" "); st.write(" "); st.write(" ")
frag2()
