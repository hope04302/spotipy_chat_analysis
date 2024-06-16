import streamlit as st
from common_container import menu
from data_analysis import song_df, BASIC_COL, rank_df

import pandas as pd
from collections import Counter
from data_function import YoonTokenizer
from datetime import date, timedelta

st.set_page_config(layout="wide")
menu()

st.write("# 문장의 토큰화")
st.divider()


@st.experimental_fragment
def frag1():
    st.dataframe(song_df[BASIC_COL + ['tk_lyrics']])


@st.experimental_fragment
def frag2():

    st.write("클러스터링에 앞서서 한국어는 `Okt`, 영어는 `nltk`를 이용해 토큰화")
    st.write("아래를 통해 토크나이저를 체험해보자")
    with st.container(border=True):
        tokenizer = YoonTokenizer()
        st.subheader("Tokenization Machine")
        col1, col2 = st.columns(2)
        a = col1.text_area(label="원하는 한글 + 영어 문장")
        b = col2.markdown(f"토큰화 결과:\n{tokenizer.tokenize(a)}")


frag2()
frag1()
st.write(" "); st.write(" "); st.write(" ")


st.write("# 단순 빈도 분석")
st.divider()


@st.cache_data
def most_common(start_year=2000, end_year=2023):
    counter = Counter()
    rank_interval = rank_df[rank_df["date"].dt.year.between(start_year, end_year)]
    for idx in rank_interval.index:
        song_id = rank_interval.loc[idx, "song_id"]
        counter.update(song_df.loc[song_id, "tk_full_lyrics"])
    return list(map(lambda x: (x[0], x[1]), counter.most_common(20)))


@st.experimental_fragment
def frag3():
    st.write("시대별 단어 빈도")
    txt = st.slider("check year", min_value=2000, max_value=2023, value=(2000, 2023))
    st.bar_chart(data=pd.DataFrame(most_common(txt[0], txt[1]), columns=("word", "cnt")), x="word", y="cnt", height=500)


@st.experimental_fragment
def frag4():
    st.write("전체 단어 빈도")
    counter = Counter()
    for vec in song_df["tk_full_lyrics"]:
        counter.update(vec)

    st.bar_chart(data=pd.DataFrame(counter.most_common()[:30], columns=("word", "cnt")), x="word", y="cnt", height=500)


frag3()
frag4()
